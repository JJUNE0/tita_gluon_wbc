// Bounded zero-torque finalization on orderly control-loop exit, including exceptions.
// No SDK/ROS dependency; callbacks execute on the existing sole motor writer thread.
#pragma once
#include <cstddef>
#include <exception>

namespace tita
{
struct ControlLoopExit
{
  std::exception_ptr loop_error;
  bool zero_requested{false}, zero_failed{false};
  std::size_t attempts{0}, accepted{0};
};

// A disabled output gate must stay command-free, including after a CAN failure.
// Transport acceptance is not a motor acknowledgement or power isolation.
// SIGKILL, power loss, a stuck writer and a broken CAN link cannot be covered here.
template<class Work, class SendZero, class Wait>
ControlLoopExit run_with_torque_release(
  Work work, bool & output_enabled, SendZero send_zero, Wait wait) noexcept
{
  ControlLoopExit result;
  try {work();} catch (...) {result.loop_error = std::current_exception();}
  if (output_enabled) {
    result.zero_requested = true;
    constexpr std::size_t repetitions = 10;
    for (std::size_t i = 0; i < repetitions; ++i) {
      ++result.attempts;
      bool sent = false;
      try {sent = send_zero();} catch (...) {}
      if (!sent) {result.zero_failed = true; break;}
      ++result.accepted;
      if (i + 1 < repetitions) {
        try {wait();} catch (...) {result.zero_failed = true; break;}
      }
    }
  }
  output_enabled = false;
  return result;
}
}  // namespace tita
