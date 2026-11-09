// Nonblocking motor/worker exchange. This file has no ROS, SDK, CAN or ONNX dependency.
#pragma once

#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstdint>
#include <functional>
#include <mutex>
#include <string>
#include <thread>
#include "tita_controller/adapter.hpp"

namespace tita
{
inline uint64_t policy_now_ns()
{
  return static_cast<uint64_t>(std::chrono::duration_cast<std::chrono::nanoseconds>(
    std::chrono::steady_clock::now().time_since_epoch()).count());
}

struct PolicyInput
{
  RobotState state;
  std::array<double, 3> command{};
  std::array<float, 8> applied_action{};
  Joints applied_residual{};
  uint64_t control_tick{0}, sensed_ns{0}, epoch{0}, stop_epoch{0};
  double gyro_bias{0.};
  bool rl{false}, stop_allowed{false};
};

struct PolicyOutput
{
  PolicyInput source;
  std::array<float, 38> observation{};
  std::array<float, 8> action{};
  Joints residual{};
  std::array<double, 3> latch_velocity_estimate{};
  double residual_wheel_position_error_m{0.};
  bool residual_position_latched{false};
  uint64_t sequence{0}, started_ns{0}, completed_ns{0};
  uint64_t teacher_source_ns{0}, teacher_source_tick{0};
  double observation_us{0.}, teacher_us{0.}, residual_us{0.};
  bool teacher_updated{false}, residual_updated{false};
};

// No caller waits for a mutex: a contended exchange is skipped. ONNX, allocation,
// callbacks and I/O never run with this mailbox locked. Values have fixed size.
template<class T> class LatestPolicyValue
{
public:
  bool publish(const T & value)
  {
    std::unique_lock<std::mutex> lock(mutex_, std::try_to_lock);
    if (!lock.owns_lock()) return false;
    value_ = value;
    available_ = true;
    return true;
  }
  bool read(T & value)
  {
    std::unique_lock<std::mutex> lock(mutex_, std::try_to_lock);
    if (!lock.owns_lock() || !available_) return false;
    value = value_;
    return true;
  }
private:
  std::mutex mutex_;
  T value_{};
  bool available_{false};
};

class AsyncPolicyWorker
{
public:
  using Processor = std::function<PolicyOutput(const PolicyInput &)>;
  using Observer = std::function<void(const PolicyOutput &)>;
  explicit AsyncPolicyWorker(Processor process, Observer observe = {},
    std::chrono::microseconds period = std::chrono::microseconds(4000))
  : process_(std::move(process)), observe_(std::move(observe)), period_(checked_period(period)), thread_([this] {run();}) {}
  ~AsyncPolicyWorker() {stop();}
  AsyncPolicyWorker(const AsyncPolicyWorker &) = delete;
  AsyncPolicyWorker & operator=(const AsyncPolicyWorker &) = delete;

  bool submit(const PolicyInput & input) {return input_.publish(input);}
  bool poll(PolicyOutput & output) {return output_.read(output);}
  bool failed() const {return failed_.load(std::memory_order_acquire);}
  const std::string & error() const {return error_;}  // Read only after failed().
  void stop()
  {
    running_.store(false);
    wake_.notify_one();
    if (thread_.joinable()) thread_.join();
  }

private:
  static std::chrono::microseconds checked_period(std::chrono::microseconds period)
  {
    if (period.count() != 4000 && period.count() != 20000) throw std::runtime_error("invalid policy worker period");
    return period;
  }
  void run() noexcept
  {
    try {
      auto next = std::chrono::steady_clock::now();
      uint64_t sequence = 0, previous_tick = 0, previous_epoch = 0;
      bool processed = false;
      while (running_.load()) {
        PolicyInput input;
        if (input_.read(input) && (!processed || input.control_tick != previous_tick || input.epoch != previous_epoch)) {
          previous_tick = input.control_tick;
          previous_epoch = input.epoch;
          processed = true;
          auto output = process_(input);
          output.sequence = ++sequence;
          output_.publish(output);
          if (observe_) observe_(output);
        }
        next += period_;
        const auto now = std::chrono::steady_clock::now();
        // Drop missed inference slots; do not replay stale snapshots in a burst.
        if (next <= now) next = now + period_;
        std::unique_lock<std::mutex> lock(sleep_mutex_);
        wake_.wait_until(lock, next, [this] {return !running_.load();});
      }
    } catch (const std::exception & error) {
      error_ = error.what();
      failed_.store(true, std::memory_order_release);
    } catch (...) {
      error_ = "unknown policy worker exception";
      failed_.store(true, std::memory_order_release);
    }
  }
  Processor process_;
  Observer observe_;
  std::chrono::microseconds period_;
  LatestPolicyValue<PolicyInput> input_;
  LatestPolicyValue<PolicyOutput> output_;
  std::atomic<bool> running_{true}, failed_{false};
  std::string error_;
  std::mutex sleep_mutex_;
  std::condition_variable wake_;
  std::thread thread_;
};

struct PolicyDecision
{
  bool valid{false}, pending{false}, fault{false}, residual_valid{false};
  std::array<float, 8> action{};
  Joints residual{};
};

class PolicyMotorBridge
{
public:
  static constexpr uint64_t kResidualMaxAgeNs = 12000000;  // Three residual periods.
  static constexpr uint64_t kTeacherMaxAgeNs = 40000000;   // Two Teacher periods.
  explicit PolicyMotorBridge(uint64_t residual_max_age_ns = kResidualMaxAgeNs)
  : residual_max_age_ns_(residual_max_age_ns)
  {
    if (!residual_max_age_ns || residual_max_age_ns > kTeacherMaxAgeNs) throw std::runtime_error("invalid residual freshness limit");
  }
  void begin(uint64_t epoch, uint64_t now)
  {
    epoch_ = epoch;
    entered_ns_ = now;
    have_output_ = false;
  }
  void accept(const PolicyOutput & output)
  {
    if (output.source.epoch == epoch_ && (!have_output_ || output.sequence > output_.sequence)) {
      output_ = output;
      have_output_ = true;
    }
  }
  PolicyDecision decide(uint64_t now, uint64_t stop_epoch, bool rl, bool stop_allowed, bool failed) const
  {
    PolicyDecision result;
    if (!rl) return result;
    if (failed) {result.fault = true; return result;}
    if (!have_output_ || !output_.source.rl) {
      result.pending = now >= entered_ns_ && now-entered_ns_ <= kTeacherMaxAgeNs;
      result.fault = !result.pending;
      return result;
    }
    if (!fresh(now, output_.teacher_source_ns, kTeacherMaxAgeNs) ||
      !fresh(now, output_.source.sensed_ns, kTeacherMaxAgeNs))
    {
      result.fault = true;
      return result;
    }
    result.valid = true;
    result.action = output_.action;
    if (stop_allowed && output_.source.stop_allowed && output_.source.stop_epoch == stop_epoch &&
      fresh(now, output_.source.sensed_ns, residual_max_age_ns_))
    {
      result.residual = output_.residual;
      result.residual_valid = true;
    }
    return result;
  }
  const PolicyOutput * output() const {return have_output_ ? &output_ : nullptr;}
private:
  static bool fresh(uint64_t now, uint64_t source, uint64_t limit)
  {
    return source != 0 && now >= source && now-source <= limit;
  }
  uint64_t epoch_{0}, entered_ns_{0};
  uint64_t residual_max_age_ns_;
  bool have_output_{false};
  PolicyOutput output_{};
};
}  // namespace tita
