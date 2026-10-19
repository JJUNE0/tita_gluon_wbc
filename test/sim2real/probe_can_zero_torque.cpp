// ROBOT_COMMAND_FREE_RUNTIME: read mode. ROBOT_STATE_CHANGING: zero mode.
// Bounded SDK transport probe: never sends nonzero torque, gains or pose targets.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <csignal>
#include <cstdlib>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

#include "tita_robot/tita_robot.hpp"

volatile std::sig_atomic_t stop_requested = 0;
void stop(int) {stop_requested = 1;}

int main(int argc, char ** argv)
{
  if (argc != 4 || (std::string(argv[1]) != "read" && std::string(argv[1]) != "zero")) {
    std::cerr << "Usage: probe_can_zero_torque read|zero RATE_HZ DURATION_SECONDS\n";
    return 2;
  }
  const bool send = std::string(argv[1]) == "zero";
  const double rate = std::stod(argv[2]), seconds = std::stod(argv[3]);
  if (!std::isfinite(rate) || rate < 1 || rate > 500 ||
    !std::isfinite(seconds) || seconds <= 0 || seconds > 2) return 2;
  std::signal(SIGINT, stop);
  std::signal(SIGTERM, stop);
  std::cout << "Execution Domain: " << (send ? "ROBOT_STATE_CHANGING" : "ROBOT_COMMAND_FREE_RUNTIME")
            << "; mode=" << argv[1] << "; rate_hz=" << rate << "; seconds=" << seconds << std::endl;
  tita_robot robot(8);
  std::this_thread::sleep_for(std::chrono::milliseconds(200));
  if (robot.imu_data_timeout() || robot.motors_data_timeout()) {
    std::cerr << "FAIL stale initial sensors; no torque commands sent" << std::endl;
    std::_Exit(3);
  }
  auto print = [](const char * label, const std::vector<double> & values) {
      std::cout << label;
      for (double value : values) std::cout << ' ' << value;
      std::cout << std::endl;
    };
  print("initial_q", robot.get_joint_q());
  print("initial_dq", robot.get_joint_v());
  print("initial_measured_t", robot.get_joint_t());
  const auto start = std::chrono::steady_clock::now();
  const auto period = std::chrono::duration_cast<std::chrono::steady_clock::duration>(
    std::chrono::duration<double>(1. / rate));
  auto next = start;
  unsigned calls = 0;
  bool failed = false;
  double max_call_ms = 0.;
  while (!stop_requested && std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count() < seconds) {
    if (robot.imu_data_timeout() || robot.motors_data_timeout()) {
      std::cerr << "FAIL stale sensors; stopping" << std::endl;
      failed = true;
      break;
    }
    const auto velocity = robot.get_joint_v();
    if (velocity.size() != 8 || !std::all_of(velocity.begin(), velocity.end(),
      [](double v) {return std::isfinite(v) && std::abs(v) < 5.;})) {
      std::cerr << "FAIL invalid/fast joint velocity; stopping" << std::endl;
      failed = true;
      break;
    }
    if (send) {
      const auto before = std::chrono::steady_clock::now();
      bool ok = false;
      try {ok = robot.set_target_joint_t(std::vector<double>(8, 0.));}
      catch (const std::exception & e) {std::cerr << "SDK exception: " << e.what() << std::endl;}
      max_call_ms = std::max(max_call_ms, std::chrono::duration<double, std::milli>(
          std::chrono::steady_clock::now() - before).count());
      ++calls;
      if (!ok) {
        std::cerr << "FAIL send at call=" << calls << "; no retries" << std::endl;
        failed = true;
        break;
      }
    }
    // Skip missed deadlines; never catch up by sending a burst.
    next = std::max(next + period, std::chrono::steady_clock::now());
    std::this_thread::sleep_until(next);
  }
  print("final_dq", robot.get_joint_v());
  std::cout << "result=" << (failed ? "FAIL" : stop_requested ? "INTERRUPTED" : "PASS")
            << "; calls=" << calls << "; max_call_ms=" << max_call_ms
            << "; elapsed_seconds=" << std::chrono::duration<double>(
      std::chrono::steady_clock::now() - start).count() << std::endl;
  // The SDK destructor hung after the read-only probe completed. This standalone
  // diagnostic intentionally exits after flushing its result; the OS closes its
  // sockets and threads. No final torque command is added here.
  std::_Exit(failed ? 1 : stop_requested ? 130 : 0);
}
