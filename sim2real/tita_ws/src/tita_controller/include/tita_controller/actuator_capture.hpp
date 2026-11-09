// Fixed-size, single-producer/single-consumer telemetry. No ROS/SDK/I/O on push.
#pragma once
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <functional>
#include <thread>
#include "tita_controller/adapter.hpp"

namespace tita
{
// Teacher-only references remain selected between 50 Hz inferences. Logging
// validity must follow that hold, rather than only the current inference tick.
struct SynchronousCaptureTrace
{
  uint64_t source_ns{0}, started_ns{0}, completed_ns{0};
  bool valid{false};
  void observe_rl(bool rl) {if (!rl) valid = false;}
  void complete(uint64_t source, uint64_t completed)
  {source_ns = source; completed_ns = completed; valid = true;}
};

struct ActuatorRecord
{
  int64_t ros_ns{0};
  uint64_t sequence{0}, tick{0}, sensed_ns{0}, read_begin_ns{0}, feedback_read_ns{0};
  uint64_t command_begin_ns{0}, command_end_ns{0}, previous_command_ns{0};
  uint64_t policy_sequence{0}, policy_source_ns{0}, teacher_source_ns{0};
  uint64_t policy_started_ns{0}, policy_completed_ns{0};
  uint64_t policy_epoch{0}, residual_epoch{0}, dropped{0};
  double loop_us{0.}, deadline_late_us{0.};
  uint8_t state{0};
  bool sensors_valid{false}, feedback_valid{false}, policy_valid{false}, reference_valid{false};
  bool output_enabled{false}, sent{false}, previous_sent{false}, asynchronous{false};
  bool residual_valid{false}, residual_action{false}, residual_allowed{false};
  Joints q{}, dq{}, reference_q{}, reference_dq{}, torque{}, reported{}, previous_torque{};
  Joints kp{}, kd{}, limits{}, residual{};
  Joints filtered_residual{};
  double residual_lpf_hz{0.};
  std::array<float, 8> teacher_action{}, applied_action{};
  std::array<double, 4> quat{};
  std::array<double, 3> gyro{}, command{}, pose{};
};

template<class T, std::size_t Capacity> class CaptureQueue
{
  static_assert(Capacity > 1, "capture queue needs two or more slots");
public:
  bool push(const T & value)
  {
    const auto write = write_.load(std::memory_order_relaxed);
    if (write-read_.load(std::memory_order_acquire) == Capacity) return false;
    values_[write % Capacity] = value;
    write_.store(write+1, std::memory_order_release);
    return true;
  }
  bool pop(T & value)
  {
    const auto read = read_.load(std::memory_order_relaxed);
    if (read == write_.load(std::memory_order_acquire)) return false;
    value = values_[read % Capacity];
    read_.store(read+1, std::memory_order_release);
    return true;
  }
private:
  std::array<T, Capacity> values_{};
  alignas(64) std::atomic<std::size_t> write_{0};
  alignas(64) std::atomic<std::size_t> read_{0};
};

class ActuatorCapture
{
public:
  explicit ActuatorCapture(std::function<void(const ActuatorRecord &)> publish)
  : publish_(std::move(publish)), thread_([this] {run();}) {}
  ~ActuatorCapture() {stop();}
  bool push(const ActuatorRecord & record)
  {
    if (queue_.push(record)) {++accepted_; return true;}
    ++dropped_; return false;
  }
  void stop()
  {
    running_ = false;
    if (thread_.joinable()) thread_.join();
  }
  uint64_t accepted() const {return accepted_;}
  uint64_t dropped() const {return dropped_;}
  uint64_t published() const {return published_;}
  uint64_t errors() const {return errors_;}
private:
  void run()
  {
    for (;;) {
      ActuatorRecord record;
      if (queue_.pop(record)) {
        try {publish_(record); ++published_;}
        catch (...) {++errors_;}  // Telemetry failure cannot terminate motor control.
      } else if (!running_.load()) {break;}
      else {std::this_thread::sleep_for(std::chrono::milliseconds(1));}
    }
  }
  CaptureQueue<ActuatorRecord, 2048> queue_;
  std::function<void(const ActuatorRecord &)> publish_;
  std::atomic<bool> running_{true};
  std::atomic<uint64_t> accepted_{0}, dropped_{0}, published_{0}, errors_{0};
  std::thread thread_;
};
}  // namespace tita
