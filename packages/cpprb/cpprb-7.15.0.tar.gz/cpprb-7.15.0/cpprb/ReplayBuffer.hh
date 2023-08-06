#ifndef YMD_REPLAY_BUFFER_HH
#define YMD_REPLAY_BUFFER_HH 1

#include <cmath>
#include <vector>
#include <random>
#include <utility>
#include <deque>
#include <tuple>
#include <functional>
#include <type_traits>
#include <limits>
#include <atomic>
#include <memory>
#include <mutex>

#include "SegmentTree.hh"

namespace ymd {

  template<typename Buffer> inline void clear(Buffer* b){ b->clear(); }
  template<typename Buffer>
  inline std::size_t get_next_index(Buffer* b){ return b->get_next_index(); }
  template<typename Buffer>
  inline std::size_t get_buffer_size(Buffer* b){ return b->get_buffer_size(); }
  template<typename Buffer>
  inline std::size_t get_stored_size(Buffer* b){ return b->get_stored_size(); }

  template<typename T>
  class DimensionalBuffer {
  private:
    T* buffer;
    const std::size_t buffer_size;
    const std::size_t dim;
    std::shared_ptr<T[]> view;
    std::size_t index(std::size_t ith) const noexcept { return ith * dim; }
    T* access(std::size_t ith) const noexcept { return buffer + index(ith); }
  public:
    DimensionalBuffer(std::size_t size,std::size_t dim,T* pointer=nullptr)
      : buffer{pointer},
	buffer_size(size),
	dim{dim},
	view{}
    {
      if(!buffer){
	buffer = new T[size * dim]{};
	view.reset(buffer);
      }
    }
    DimensionalBuffer(): DimensionalBuffer{std::size_t(1),std::size_t(1)}  {}
    DimensionalBuffer(const DimensionalBuffer& other) = default;
    DimensionalBuffer(DimensionalBuffer&& other) = default;
    DimensionalBuffer& operator=(const DimensionalBuffer&) = default;
    DimensionalBuffer& operator=(DimensionalBuffer&&) = default;
    virtual ~DimensionalBuffer() = default;
    template<typename V,
	     std::enable_if_t<std::is_convertible_v<V,T>,std::nullptr_t> = nullptr>
    void store_data(V* v,std::size_t shift,std::size_t next_index,std::size_t N){
      std::copy_n(v + index(shift), N*dim,access(next_index));
    }
    void get_data(std::size_t ith,std::vector<T>& v) const {
      std::copy(access(ith), access(ith+1),std::back_inserter(v));
    }
    void get_data(std::size_t ith,std::vector<std::vector<T>>& v) const {
      v.emplace_back(access(ith),access(ith+1));
    }
    void get_data(std::size_t ith,T*& v) const {
      v = access(ith);
    }
    std::size_t get_buffer_size() const noexcept { return buffer_size; }
  };

  template<typename Observation,typename Action,typename Reward,typename Done>
  class Environment {
  private:
    const std::size_t buffer_size;
    const std::size_t obs_dim;
    const std::size_t act_dim;
    DimensionalBuffer<Observation> obs_buffer;
    DimensionalBuffer<Action> act_buffer;
    DimensionalBuffer<Reward> rew_buffer;
    DimensionalBuffer<Observation> next_obs_buffer;
    DimensionalBuffer<Done> done_buffer;
  public:
    Environment(std::size_t size,
		std::size_t obs_dim,std::size_t act_dim,std::size_t rew_dim = 1,
		Observation* obs=nullptr,Action* act=nullptr,Reward* rew=nullptr,
		Observation* next_obs=nullptr,Done* done=nullptr)
      : buffer_size{size},
	obs_dim{obs_dim},
	act_dim{act_dim},
	obs_buffer{size,obs_dim,obs},
	act_buffer{size,act_dim,act},
	rew_buffer{size,rew_dim,rew},
	next_obs_buffer{size,obs_dim,next_obs},
	done_buffer{size,std::size_t(1),done} {}
    Environment(): Environment{std::size_t(1),std::size_t(1),std::size_t(1)} {}
    Environment(const Environment&) = default;
    Environment(Environment&&) = default;
    Environment& operator=(const Environment&) = default;
    Environment& operator=(Environment&&) = default;
    virtual ~Environment() = default;
    template<typename Obs_t,typename Act_t,typename Rew_t,
	     typename Next_Obs_t,typename Done_t>
    void store(Obs_t* obs,Act_t* act, Rew_t* rew,
	       Next_Obs_t* next_obs,Done_t* done,
	       std::size_t shift = std::size_t(0),
	       std::size_t index = std::size_t(0), size_t N = std::size_t(1)){
      obs_buffer     .store_data(     obs,shift,index,N);
      act_buffer     .store_data(     act,shift,index,N);
      rew_buffer     .store_data(     rew,shift,index,N);
      next_obs_buffer.store_data(next_obs,shift,index,N);
      done_buffer    .store_data(    done,shift,index,N);
    }
    template<typename Obs_t,typename Act_t,typename Rew_t,typename Done_t>
    void get(std::size_t index,Obs_t& obs,Act_t& act,Rew_t& rew,
	     Obs_t& next_obs,Done_t& done) const {
      obs_buffer     .get_data(index,     obs);
      act_buffer     .get_data(index,     act);
      rew_buffer     .get_data(index,     rew);
      next_obs_buffer.get_data(index,next_obs);
      done_buffer    .get_data(index,    done);
    }

    void get_buffer_pointers(Observation*& obs, Action*& act, Reward*& rew,
			     Observation*& next_obs, Done*& done) const {
      get(std::size_t(0),obs,act,rew,next_obs,done);
    }
    std::size_t get_buffer_size() const noexcept { return buffer_size; }
  };

  template<bool MultiThread,typename T> struct ThreadSafe{
    using type = std::atomic<T>;
    static inline auto fetch_add(volatile type* v,T N,const std::memory_order& order){
      return v->fetch_add(N,order);
    }
    static inline auto store(volatile type* v,T N,const std::memory_order& order){
      v->store(N,order);
    }
    static inline auto load(const volatile type* v,const std::memory_order& order){
      return v->load(order);
    }
    static inline auto store_max(volatile type* v,T N){
      auto tmp = v->load(std::memory_order_acquire);
      while(tmp < N &&  !v->compare_exchange_weak(tmp,N)){}
    }
  };

  template<typename T> struct ThreadSafe<false,T>{
    using type = T;
    static inline auto fetch_add(T* v,T N,const std::memory_order){
      return std::exchange(*v,(*v + N));
    }
    static inline auto store(T* v,T N,const std::memory_order&){
      *v = N;
    }
    static inline auto load(const T* v,const std::memory_order&){
      return *v;
    }
    static inline auto store_max(T* v,T N){
      if(*v < N){ *v = N; }
    }
  };

  template<typename Observation,typename Action,typename Reward,typename Done,
	   bool MultiThread = false>
  class CppRingEnvironment :public Environment<Observation,Action,Reward,Done>{
  public:
    using Env_t = Environment<Observation,Action,Reward,Done>;
    using ThreadSafe_size_t = ThreadSafe<MultiThread,std::size_t>;

  private:
    typename ThreadSafe_size_t::type *stored_size;
    typename ThreadSafe_size_t::type *next_index;
    std::shared_ptr<typename ThreadSafe_size_t::type> stored_view;
    std::shared_ptr<typename ThreadSafe_size_t::type> index_view;
    const std::size_t mask;
  public:
    CppRingEnvironment(std::size_t size,
		       std::size_t obs_dim,std::size_t act_dim,std::size_t rew_dim=1,
		       std::size_t* size_ptr=nullptr,std::size_t* index_ptr=nullptr,
		       Observation* obs=nullptr,Action* act=nullptr,
		       Reward* rew=nullptr,
		       Observation* next_obs=nullptr,Done* done=nullptr)
      : Env_t{PowerOf2(size),obs_dim,act_dim,rew_dim,obs,act,rew,next_obs,done},
	stored_size{(typename ThreadSafe_size_t::type*)size_ptr},
	next_index{(typename ThreadSafe_size_t::type*)index_ptr},
	stored_view{},
	index_view{},
	mask{ PowerOf2(size)-1 }
    {
      if(!size_ptr){
	stored_size = new typename ThreadSafe_size_t::type{};
	stored_view.reset(stored_size);
      }
      if(!index_ptr){
	next_index = new typename ThreadSafe_size_t::type{};
	index_view.reset(next_index);
      }
    }
    CppRingEnvironment(): CppRingEnvironment{std::size_t(1),
					     std::size_t(1),
					     std::size_t(1)} {}
    CppRingEnvironment(const CppRingEnvironment&) = default;
    CppRingEnvironment(CppRingEnvironment&&) = default;
    CppRingEnvironment& operator=(const CppRingEnvironment&) = default;
    CppRingEnvironment& operator=(CppRingEnvironment&&) = default;
    virtual ~CppRingEnvironment() = default;
    template<typename Obs_t,typename Act_t,typename Rew_t,
	     typename Next_Obs_t,typename Done_t>
    std::size_t store(Obs_t* obs, Act_t* act, Rew_t* rew,
		      Next_Obs_t* next_obs, Done_t* done,
		      std::size_t N = std::size_t(1)){
      constexpr const std::size_t zero = 0;
      constexpr const auto order
	= MultiThread ? std::memory_order_acquire : std::memory_order_relaxed;

      const auto buffer_size = this->get_buffer_size();

      ThreadSafe_size_t::fetch_add(stored_size,N,std::memory_order_relaxed);

      std::size_t shift = zero;
      std::size_t tmp_next_index{ThreadSafe_size_t::fetch_add(next_index,N,order) &
				 mask};
      auto stored_index = tmp_next_index;
      while(N){
	auto copy_N = std::min(N,buffer_size - tmp_next_index);

	this->Env_t::store(obs,act,rew,next_obs,done,shift,tmp_next_index,copy_N);

	N = (N > copy_N) ? N - copy_N: zero;
	shift += copy_N;
	tmp_next_index = zero;
      }
      return stored_index;
    }

    std::size_t get_stored_size(){
      auto size = ThreadSafe_size_t::load(stored_size,std::memory_order_acquire);
      const auto buffer_size = this->get_buffer_size();

      if(size < buffer_size){ return size; }

      ThreadSafe_size_t::store(stored_size,buffer_size,std::memory_order_release);
      return buffer_size;
    }
    std::size_t get_next_index() const {
      if constexpr (MultiThread){
        return next_index->load(std::memory_order_acquire) & mask;
      }else{
	return (*next_index) & mask;
      }
    }

    virtual void clear(){
      if constexpr (MultiThread){
	stored_size->store(0);
	next_index->store(0);
      }else{
	*stored_size = 0;
	*next_index = 0;
      }
    }
  };

  template<typename Observation,typename Action,typename Reward,typename Done>
  using CppThreadSafeRingEnvironment =
    CppRingEnvironment<Observation,Action,Reward,Done,true>;

  template<typename Observation,typename Action,typename Reward,typename Done>
  class CppSelectiveEnvironment :public Environment<Observation,Action,Reward,Done>{
  public:
    using Env_t = Environment<Observation,Action,Reward,Done>;

  private:
    std::size_t next_index;
    const std::size_t episode_len;
    const std::size_t Nepisodes;
    std::vector<std::size_t> episode_begins;

  public:
    CppSelectiveEnvironment(std::size_t episode_len,std::size_t Nepisodes,
			    std::size_t obs_dim,std::size_t act_dim,
			    std::size_t rew_dim=1)
      : Env_t{episode_len * Nepisodes,obs_dim,act_dim,rew_dim},
	next_index{std::size_t(0)},
	episode_len{episode_len},
	Nepisodes{Nepisodes},
	episode_begins{std::size_t(0)} {
	  episode_begins.reserve(Nepisodes);
	}
    CppSelectiveEnvironment(): CppSelectiveEnvironment{std::size_t(1),
						       std::size_t(1),
						       std::size_t(1),
						       std::size_t(1)} {}
    CppSelectiveEnvironment(const CppSelectiveEnvironment&) = default;
    CppSelectiveEnvironment(CppSelectiveEnvironment&&) = default;
    CppSelectiveEnvironment& operator=(const CppSelectiveEnvironment&) = default;
    CppSelectiveEnvironment& operator=(CppSelectiveEnvironment&&) = default;
    ~CppSelectiveEnvironment() = default;

    template<typename Obs_t,typename Act_t,typename Rew_t,
	     typename Next_Obs_t,typename Done_t>
    std::size_t store(Obs_t* obs,Act_t* act,Rew_t* rew,
		      Next_Obs_t* next_obs, Done_t* done,
		      std::size_t N = std::size_t(1)){
      const auto buffer_size = this->get_buffer_size();
      auto shift = std::size_t(0);
      auto copy_N = std::min(N,buffer_size - next_index);
      this->Env_t::store(obs,act,rew,next_obs,done,shift,next_index,copy_N);

      if(auto done_index = std::find_if(done,done+copy_N,[](auto d){ return d; });
	 done_index != done + copy_N){
	episode_begins.emplace_back(next_index
				    + std::distance(done,done_index)
				    + std::size_t(1));
      }

      return std::exchange(next_index,next_index + copy_N);
    }

    void get_episode(std::size_t i,std::size_t& ep_len,
		     Observation*& obs,Action*& act,Reward*& rew,
		     Observation*& next_obs,Done*& done) const {
      if(i >= get_stored_episode_size()){
	ep_len = std::size_t(0);
	return;
      }

      auto begin = episode_begins[i];
      this->Env_t::get(begin,obs,act,rew,next_obs,done);

      auto end = (i+1 < episode_begins.size()) ? episode_begins[i+1]: next_index;
      ep_len = end - begin;
    }

    auto get_episode(std::size_t i) const {
      Observation *obs,*next_obs;
      Action* act;
      Reward* rew;
      Done* done;
      std::size_t ep_len;
      get_episode(i,ep_len,obs,act,rew,next_obs,done);
      return std::make_tuple(obs,act,rew,next_obs,done,ep_len);
    }

    std::size_t delete_episode(std::size_t i){
      if(i > episode_begins.size() -1){
	return std::size_t(0);
      }

      if(i == episode_begins.size() -1){
	auto old_index = std::exchange(next_index,episode_begins.back());
	return old_index - next_index;
      }

      auto delete_begin = episode_begins[i];
      auto move_begin = episode_begins[i+1];
      auto move_end = next_index;

      if(move_begin == move_end){
	next_index = delete_begin;
	episode_begins.pop_back();
	return move_begin - delete_begin;
      }

      Observation *delete_obs,*move_obs,*end_obs;
      Observation *delete_next_obs,*move_next_obs,*end_next_obs;
      Action *delete_act,*move_act,*end_act;
      Reward *delete_rew,*move_rew,*end_rew;
      Done *delete_done,*move_done,*end_done;

      this->Env_t::get(delete_begin,
		       delete_obs,delete_act,delete_rew,delete_next_obs,delete_done);
      this->Env_t::get(move_begin,
		       move_obs,move_act,move_rew,move_next_obs,move_done);
      this->Env_t::get(move_end,end_obs,end_act,end_rew,end_next_obs,end_done);

      std::move(move_obs,end_obs,delete_obs);
      std::move(move_act,end_act,delete_act);
      std::move(move_rew,end_rew,delete_rew);
      std::move(move_next_obs,end_next_obs,delete_next_obs);
      std::move(move_done,end_done,delete_done);

      std::size_t delete_size = move_begin - delete_begin;
      next_index -= delete_size;
      std::transform(episode_begins.begin() + i+1, episode_begins.end(),
		     episode_begins.begin() + i,
		     [delete_size](auto begin){ return begin - delete_size; });
      episode_begins.pop_back();
      return delete_size;
    }
    std::size_t get_next_index() const { return next_index; }
    std::size_t get_stored_size() const { return next_index; }
    auto get_stored_episode_size() const {
      constexpr const std::size_t zero(0), one(1);
      return episode_begins.size() - ((next_index==episode_begins.back())? one: zero);
    }
    virtual void clear(){
      next_index = std::size_t(0);
      episode_begins.resize(1);
    }
  };

  template<typename Observation,typename Action,typename Reward,typename Done>
  class CppReplayBuffer : public CppRingEnvironment<Observation,Action,Reward,Done>{
  public:
    using Buffer_t = CppRingEnvironment<Observation,Action,Reward,Done>;
    using rand_t = std::uniform_int_distribution<std::size_t>;
  private:
    std::vector<std::size_t> index_buffer;

  protected:
    std::mt19937 g;

    auto initialize_space(std::size_t size = std::size_t(0)) const {
      std::vector<std::vector<Observation>> obs{},next_obs{};
      std::vector<std::vector<Action>> act{};
      std::vector<Reward> rew{};
      std::vector<Done> done{};

      obs.reserve(size);
      act.reserve(size);
      rew.reserve(size);
      next_obs.reserve(size);
      done.reserve(size);

      return std::make_tuple(obs,act,rew,next_obs,done);
    }

    template<typename Obs_t,typename Act_t>
    void encode_sample(const std::vector<std::size_t>& indexes,
		       Obs_t& obs, Act_t& act,
		       std::vector<Reward>& rew,
		       Obs_t& next_obs,
		       std::vector<Done>& done) const {
      obs.resize(0);
      act.resize(0);
      rew.resize(0);
      next_obs.resize(0);
      done.resize(0);

      for(auto i : indexes){
	this->get(i,obs,act,rew,next_obs,done);
      }
    }

    auto encode_sample(const std::vector<std::size_t>& indexes) const {
      auto [obs,act,rew,next_obs,done] = initialize_space(indexes.size());

      encode_sample(indexes,obs,act,rew,next_obs,done);
      return std::make_tuple(obs,act,rew,next_obs,done);
    }

  public:
    CppReplayBuffer(std::size_t n,std::size_t obs_dim,std::size_t act_dim,
		    std::size_t rew_dim = 1)
      : Buffer_t{n,obs_dim,act_dim,rew_dim},
	index_buffer{},
	g{std::random_device{}()} {}
    CppReplayBuffer(Buffer_t&& buffer)
      : Buffer_t{buffer},
	index_buffer{},
	g{std::random_device{}()} {}
    CppReplayBuffer(): CppReplayBuffer{1,1,1} {}
    CppReplayBuffer(const CppReplayBuffer&) = default;
    CppReplayBuffer(CppReplayBuffer&&) = default;
    CppReplayBuffer& operator=(const CppReplayBuffer&) = default;
    CppReplayBuffer& operator=(CppReplayBuffer&&) = default;
    virtual ~CppReplayBuffer() = default;

    virtual std::size_t add(Observation* obs,
			    Action* act,
			    Reward* rew,
			    Observation* next_obs,
			    Done* done,
			    std::size_t N = std::size_t(1)){
      return this->Buffer_t::store(obs,act,rew,next_obs,done,N);
    }

    template<typename Obs_t,typename Act_t,typename  Rew_t,typename Done_t>
    void sample(std::size_t batch_size,
		Obs_t& obs, Act_t& act,
		Rew_t& rew, Obs_t& next_obs, Done_t& done,
		std::vector<size_t>& indexes){
      auto random = [this,
		     d=rand_t{0,this->Buffer_t::get_stored_size()-1}]()mutable{
		      return d(this->g);
		    };
      indexes.resize(0);
      indexes.reserve(batch_size);
      std::generate_n(std::back_inserter(indexes),batch_size,random);

      encode_sample(indexes,obs,act,rew,next_obs,done);
    }

    template<typename Obs_t,typename Act_t,typename  Rew_t,typename Done_t>
    void sample(std::size_t batch_size,
		Obs_t& obs, Act_t& act,
		Rew_t& rew, Obs_t& next_obs, Done_t& done){
      sample(batch_size,obs,act,rew,next_obs,done,index_buffer);
    }

    auto sample(std::size_t batch_size){
      auto [obs,act,rew,next_obs,done] = initialize_space(batch_size);

      sample(batch_size,obs,act,rew,next_obs,done);

      return std::make_tuple(obs,act,rew,next_obs,done);
    }
  };

  template<typename Priority,bool MultiThread = false>
  class CppPrioritizedSampler {
  private:
    using ThreadSafePriority_t = ThreadSafe<MultiThread,Priority>;
    Priority alpha;
    typename ThreadSafePriority_t::type* max_priority;
    std::shared_ptr<typename ThreadSafePriority_t::type> max_priority_view;
    const Priority default_max_priority;
    SegmentTree<Priority,MultiThread> sum;
    SegmentTree<Priority,MultiThread> min;
    std::mt19937 g;
    Priority eps;

    void sample_proportional(std::size_t batch_size,
			     std::vector<std::size_t>& indexes,
			     std::size_t stored_size){
      indexes.resize(0);
      indexes.reserve(batch_size);

      auto every_range_len
	= Priority{1.0} * sum.reduce(0,stored_size) / batch_size;

      std::generate_n(std::back_inserter(indexes),batch_size,
		      [=,i=std::size_t(0),
		       d=std::uniform_real_distribution<Priority>{}]()mutable{
			auto mass = (d(this->g) + (i++))*every_range_len;
			return this->sum.largest_region_index([=](auto v){
								return v <= mass;
							      },stored_size);
		      });
    }

    void set_weights(const std::vector<std::size_t>& indexes,Priority beta,
		     std::vector<Priority>& weights,std::size_t stored_size) {
      weights.resize(0);
      weights.reserve(indexes.size());

      auto b_size = stored_size;
      auto inv_sum = Priority{1.0} / sum.reduce(0,b_size);
      auto p_min = min.reduce(0,b_size) * inv_sum;
      auto inv_max_weight = Priority{1.0} / std::pow(p_min * b_size,-beta);

      std::transform(indexes.begin(),indexes.end(),std::back_inserter(weights),
		     [=](auto idx){
		       auto p_sample = this->sum.get(idx) * inv_sum;
		       return std::pow(p_sample*b_size,-beta)*inv_max_weight;
		     });
    }

    template<typename F>
    void set_priorities(std::size_t next_index,F&& f,
			std::size_t N,std::size_t buffer_size){
      sum.set(next_index,std::forward<F>(f),N,buffer_size);
      min.set(next_index,std::forward<F>(f),N,buffer_size);
    }

    void set_priority(std::size_t next_index,Priority p){
      auto v = std::pow(p+eps,alpha);
      sum.set(next_index,v);
      min.set(next_index,v);
    }

  public:
    CppPrioritizedSampler(std::size_t buffer_size,Priority alpha,
			  Priority* max_p = nullptr,
			  Priority* sum_ptr = nullptr,
			  bool* sum_anychanged = nullptr,bool* sum_changed = nullptr,
			  Priority* min_ptr = nullptr,
			  bool* min_anychanged = nullptr,bool* min_changed = nullptr,
			  bool initialize = true,
			  Priority eps = Priority{1e-4})
      : alpha{alpha},
	max_priority{(typename ThreadSafePriority_t::type*)max_p},
	max_priority_view{},
	default_max_priority{1.0},
	sum{PowerOf2(buffer_size),[](auto a,auto b){ return a+b; },
	    Priority{0},
	    sum_ptr,sum_anychanged,sum_changed,initialize},
	min{PowerOf2(buffer_size),[](Priority a,Priority b){ return  std::min(a,b); },
	    std::numeric_limits<Priority>::max(),
	    min_ptr,min_anychanged,min_changed,initialize},
	g{std::random_device{}()},
	eps{eps}
    {
      if(!max_priority){
	max_priority = new typename ThreadSafePriority_t::type{};
	max_priority_view.reset(max_priority);
      }
      if(initialize){
	ThreadSafePriority_t::store(max_priority,default_max_priority,
				    std::memory_order_release);
      }
    }
    CppPrioritizedSampler(): CppPrioritizedSampler{1,0.5} {}
    CppPrioritizedSampler(const CppPrioritizedSampler&) = default;
    CppPrioritizedSampler(CppPrioritizedSampler&&) = default;
    CppPrioritizedSampler& operator=(const CppPrioritizedSampler&) = default;
    CppPrioritizedSampler& operator=(CppPrioritizedSampler&&) = default;
    ~CppPrioritizedSampler() = default;

    void sample(std::size_t batch_size,Priority beta,
		std::vector<Priority>& weights,std::vector<std::size_t>& indexes,
		std::size_t stored_size){
      sample_proportional(batch_size,indexes,stored_size);
      set_weights(indexes,beta,weights,stored_size);
    }
    virtual void clear(){
      ThreadSafePriority_t::store(max_priority,default_max_priority,
				  std::memory_order_release);
      sum.clear();
      min.clear(std::numeric_limits<Priority>::max());
    }

    Priority get_max_priority() const {
      return ThreadSafePriority_t::load(max_priority,std::memory_order_acquire);
    }

    template<typename P,
	     std::enable_if_t<std::is_convertible_v<P,Priority>,
			      std::nullptr_t> = nullptr>
    void set_priorities(std::size_t next_index,P p){
      ThreadSafePriority_t::store_max(max_priority,p);
      set_priority(next_index,p);
    }

    void set_priorities(std::size_t next_index){
      auto p = ThreadSafePriority_t::load(max_priority,std::memory_order_acquire);
      set_priority(next_index,p);
    }

    template<typename P,
	     std::enable_if_t<std::is_convertible_v<P,Priority>,
			      std::nullptr_t> = nullptr>
    void set_priorities(std::size_t next_index,P* p,
			std::size_t N,std::size_t buffer_size){
      ThreadSafePriority_t::store_max(max_priority, *std::max_element(p,p+N));

      set_priorities(next_index,
		     [=]() mutable { return std::pow(eps + *(p++),alpha); },
		     N,buffer_size);
    }

    void set_priorities(std::size_t next_index,
			std::size_t N,std::size_t buffer_size){
      const auto v = std::pow(ThreadSafePriority_t::load(max_priority,
							 std::memory_order_acquire)
			      + eps,
			      alpha);
      set_priorities(next_index,[=](){ return v; },N,buffer_size);
    }

    template<typename I,typename P,
	     std::enable_if_t<std::is_convertible_v<I,std::size_t>,
			      std::nullptr_t> = nullptr,
	     std::enable_if_t<std::is_convertible_v<P,Priority>,
			      std::nullptr_t> = nullptr>
    void update_priorities(I* indexes, P* priorities,std::size_t N =1){

      const auto max_p =
	std::accumulate(indexes,indexes+N,
			ThreadSafePriority_t::load(max_priority,
						   std::memory_order_acquire),
			[=,p=priorities]
			(auto max_p, auto index) mutable {
			  Priority v = std::pow(*p,this->alpha);
			  this->sum.set(index,v);
			  this->min.set(index,v);

			  return std::max<Priority>(max_p,*(p++));
			});
      ThreadSafePriority_t::store_max(max_priority,max_p);
    }

    template<typename I,typename P,
	     std::enable_if_t<std::is_convertible_v<I,std::size_t>,
			      std::nullptr_t> = nullptr,
	     std::enable_if_t<std::is_convertible_v<P,Priority>,
			      std::nullptr_t> = nullptr>
    void update_priorities(std::vector<I>& indexes,
			   std::vector<P>& priorities){

      update_priorities(indexes.data(),priorities.data(),
			std::min(indexes.size(),priorities.size()));
    }

    void set_eps(Priority eps){
      this->eps = eps;
    }
  };

  template<typename Priority>
  using CppThreadSafePrioritizedSampler = CppPrioritizedSampler<Priority,true>;

  template<typename Observation,typename Action,typename Reward,typename Done,
	   typename Priority>
  class CppPrioritizedReplayBuffer:
    public CppReplayBuffer<Observation,Action,Reward,Done>,
    public CppPrioritizedSampler<Priority> {
  private:
    using BaseClass = CppReplayBuffer<Observation,Action,Reward,Done>;
    using Sampler = CppPrioritizedSampler<Priority>;
  public:
    CppPrioritizedReplayBuffer(std::size_t n,std::size_t obs_dim,std::size_t act_dim,
			       std::size_t rew_dim, Priority alpha)
      : BaseClass{n,obs_dim,act_dim,rew_dim},
	Sampler{n,alpha} {}
    CppPrioritizedReplayBuffer() : CppPrioritizedReplayBuffer{1,1,1,0.0} {}
    CppPrioritizedReplayBuffer(const CppPrioritizedReplayBuffer&) = default;
    CppPrioritizedReplayBuffer(CppPrioritizedReplayBuffer&&) = default;
    CppPrioritizedReplayBuffer& operator=(const CppPrioritizedReplayBuffer&)=default;
    CppPrioritizedReplayBuffer& operator=(CppPrioritizedReplayBuffer&&) = default;
    virtual ~CppPrioritizedReplayBuffer() override = default;

    virtual std::size_t add(Observation* obs,Action* act,Reward* rew,
			    Observation* next_obs,Done* done,std::size_t N) override {
      auto next_index = this->BaseClass::add(obs,act,rew,next_obs,done,N);
      this->set_priorities(next_index,N,this->get_buffer_size());
      return next_index;
    }

    virtual std::size_t add(Observation* obs,Action* act,Reward* rew,
			    Observation* next_obs,Done* done,
			    Priority* priority,std::size_t N){
      auto next_index = this->BaseClass::add(obs,act,rew,next_obs,done,N);
      this->set_priorities(next_index,priority,N,this->get_buffer_size());
      return next_index;
    }

    virtual std::size_t add(Observation* obs,Action* act,Reward* rew,
			    Observation* next_obs,Done* done,Priority p){
      auto next_index= this->BaseClass::add(obs,act,rew,next_obs,done,std::size_t(1));
      this->set_priorities(next_index,p);
      return next_index;
    }

    virtual std::size_t add(Observation* obs,Action* act,Reward* rew,
			    Observation* next_obs,Done* done){
      auto next_index= this->BaseClass::add(obs,act,rew,next_obs,done,std::size_t(1));
      this->set_priorities(next_index);
      return next_index;
    }

    template<typename Obs_t,typename Act_t,typename Rew_t,typename Done_t>
    void sample(std::size_t batch_size,Priority beta,
		Obs_t& obs, Act_t& act,
		Rew_t& rew, Obs_t& next_obs, Done_t& done,
		std::vector<Priority>& weights,
		std::vector<std::size_t>& indexes){

      this->Sampler::sample(batch_size,beta,weights,indexes,this->get_stored_size());

      this->BaseClass::encode_sample(indexes,obs,act,rew,next_obs,done);
    }

    template<typename Obs_t,typename Act_t>
    void sample(std::size_t batch_size,
		Obs_t& obs, Act_t& act,
		std::vector<Reward>& rew,
		Obs_t& next_obs,
		std::vector<Done>& done){
      std::vector<Priority> weights{};
      std::vector<std::size_t> indexes{};
      sample(batch_size,Priority{0.0},obs,act,rew,next_obs,done,weights,indexes);
    }

    auto sample(std::size_t batch_size,Priority beta){
      beta = std::max(beta,Priority{0});

      std::vector<std::size_t> indexes{};
      indexes.reserve(batch_size);

      std::vector<Priority> weights{};
      weights.reserve(batch_size);

      this->Sampler::sample(batch_size,beta,weights,indexes,this->get_stored_size());

      auto samples = this->BaseClass::encode_sample(indexes);
      return std::tuple_cat(samples,std::make_tuple(weights,indexes));
    }

    auto sample(std::size_t batch_size){
      return sample(batch_size,Priority{0.0});
    }

    virtual void clear() override {
      this->BaseClass::clear();
      this->Sampler::clear();
    }
  };

  template<typename Observation,typename Reward>
  class CppNstepRewardBuffer {
  private:
    const std::size_t buffer_size;
    const std::size_t obs_dim;
    const std::size_t nstep;
    Reward gamma;
    std::vector<Reward> gamma_buffer;
    std::vector<Reward> nstep_rew_buffer;
    std::vector<Observation> nstep_next_obs_buffer;
    template<typename Done>
    void update_nstep(std::size_t& i,std::size_t end,
		      Reward* rew,Done* done,Reward& gamma_i){
      for(; i < end; ++i){
	gamma_i *= gamma;
	nstep_rew_buffer.back() += rew[i] * gamma_i;
	if(done[i]){ return; }
      }

      --i;
    }
    void reset_buffers(std::size_t size){
      gamma_buffer.resize(0);
      gamma_buffer.reserve(size);

      nstep_rew_buffer.resize(0);
      nstep_rew_buffer.reserve(size);

      nstep_next_obs_buffer.resize(0);
      nstep_next_obs_buffer.reserve(size*obs_dim);
    }
  public:
    CppNstepRewardBuffer(std::size_t size,std::size_t obs_dim,
			 std::size_t nstep,Reward gamma)
      : buffer_size{size},
	obs_dim{obs_dim},
	nstep{nstep},
	gamma{gamma},
	gamma_buffer{},
	nstep_rew_buffer{},
	nstep_next_obs_buffer{} {}
    CppNstepRewardBuffer() = default;
    CppNstepRewardBuffer(const CppNstepRewardBuffer&) = default;
    CppNstepRewardBuffer(CppNstepRewardBuffer&&) = default;
    CppNstepRewardBuffer& operator=(const CppNstepRewardBuffer&) = default;
    CppNstepRewardBuffer& operator=(CppNstepRewardBuffer&&) = default;
    virtual ~CppNstepRewardBuffer() = default;

    template<typename Done>
    void sample(const std::vector<std::size_t>& indexes,
		Reward* rew,Observation* next_obs,Done* done){
      constexpr const std::size_t zero = 0;
      reset_buffers(indexes.size());

      for(auto index: indexes){
	auto gamma_i = Reward{1};
	nstep_rew_buffer.push_back(rew[index]);

	auto remain = nstep - 1;
	while((!done[index]) && remain){
	  index = (index < buffer_size - 1) ? index+1: zero;

	  auto end = index + remain;
	  update_nstep(index,std::min(end,buffer_size),rew,done,gamma_i);
	  remain = (end > buffer_size) ? end - buffer_size: zero;
	}

	std::copy_n(next_obs+index*obs_dim,obs_dim,
		    std::back_inserter(nstep_next_obs_buffer));
	gamma_buffer.push_back(gamma_i);
      }
    }
    void get_buffer_pointers(Reward*& discounts,Reward*& ret,Observation*& obs){
      discounts = gamma_buffer.data();
      ret = nstep_rew_buffer.data();
      obs = nstep_next_obs_buffer.data();
    }
  };
}
#endif // YMD_REPLAY_BUFFER_HH
