// Calling-thread scheduling only. No SDK, CAN, ROS or policy dependency.
#pragma once
#include <cerrno>
#include <cstring>
#include <pthread.h>
#include <sched.h>
#include <stdexcept>
#include <string>
#include <system_error>
#include <sys/prctl.h>

namespace tita
{
inline int motor_realtime_priority(const char * environment)
{
  if (!environment || std::strcmp(environment, "20") == 0) return 20;
  if (std::strcmp(environment, "0") == 0) return 0;
  throw std::invalid_argument("TITA_MOTOR_RT_PRIORITY must be 20 or 0");
}

struct MotorSchedulingSystem
{
  static int scheduler(int * policy, sched_param * parameter)
  {return pthread_getschedparam(pthread_self(), policy, parameter);}
  static int scheduler(int policy, const sched_param * parameter)
  {return pthread_setschedparam(pthread_self(), policy, parameter);}
  static long slack() {return prctl(PR_GET_TIMERSLACK);}
  static int slack(unsigned long value) {return prctl(PR_SET_TIMERSLACK, value);}
};

// Backend parameter permits failure/rollback tests without requiring RT privileges.
template<class System = MotorSchedulingSystem> class ScopedMotorRealtime
{
public:
  ScopedMotorRealtime(bool output_enabled, int priority)
  {
    if (priority != 0 && priority != 20) throw std::invalid_argument("motor_realtime_priority must be 20 or 0");
    if (!output_enabled || priority == 0) return;
    int error = System::scheduler(&previous_policy_, &previous_parameter_);
    if (error) fail(error, "read motor thread scheduler");
    previous_slack_ = System::slack();
    if (previous_slack_ < 0) fail(errno, "read motor thread timer slack");
    if (System::slack(1UL) != 0) fail(errno, "set motor thread timer slack");
    slack_changed_ = true;
    sched_param requested{};requested.sched_priority = priority;
    error = System::scheduler(SCHED_FIFO, &requested);
    if (error) {restore();fail(error, "set motor thread SCHED_FIFO priority20");}
    scheduler_changed_ = true;
    int actual_policy{};sched_param actual{};
    error = System::scheduler(&actual_policy, &actual);
    if (error || actual_policy != SCHED_FIFO || actual.sched_priority != priority || System::slack() != 1) {
      restore();fail(error ? error : EIO, "verify motor thread scheduler/timer slack");
    }
    active_ = true;
  }
  ~ScopedMotorRealtime() {restore();}
  ScopedMotorRealtime(const ScopedMotorRealtime &) = delete;
  ScopedMotorRealtime & operator=(const ScopedMotorRealtime &) = delete;
  bool active() const {return active_;}

private:
  [[noreturn]] static void fail(int error, const char * operation)
  {
    throw std::system_error(error, std::generic_category(),
      std::string(operation) + "; motor control not started; TITA_MOTOR_RT_PRIORITY=0 selects normal scheduling");
  }
  void restore() noexcept
  {
    if (scheduler_changed_) System::scheduler(previous_policy_, &previous_parameter_);
    if (slack_changed_) System::slack(static_cast<unsigned long>(previous_slack_));
    scheduler_changed_ = slack_changed_ = active_ = false;
  }
  int previous_policy_{};
  sched_param previous_parameter_{};
  long previous_slack_{};
  bool scheduler_changed_{false}, slack_changed_{false}, active_{false};
};
}  // namespace tita
