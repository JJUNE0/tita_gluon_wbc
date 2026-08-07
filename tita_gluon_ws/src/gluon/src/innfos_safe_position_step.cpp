#include <cstdint>

#include "actuatorcontroller.h"

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <csignal>
#include <exception>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

namespace {

std::atomic<bool> stop_requested(false);

struct Options {
  int actuator_id = -1;
  double target_turns = 0.0;
  double expected_start_turns = 0.0;
  double max_start_error_turns = 0.0;
  double max_step_turns = 0.0;
  double profile_max_rpm = 0.0;
  double profile_acceleration = 0.0;
  double current_limit_a = 0.0;
  double current_abort_a = 0.0;
  int timeout_seconds = 0;
  int diagnostic_hold_seconds = 0;
  bool execute = false;
  bool confirmed = false;
};

void handle_signal(int) { stop_requested.store(true); }

double parse_double(const std::string &value, const char *name) {
  std::size_t consumed = 0;
  const double parsed = std::stod(value, &consumed);
  if (consumed != value.size() || !std::isfinite(parsed)) {
    throw std::invalid_argument(std::string(name) + " requires a finite number");
  }
  return parsed;
}

int parse_int(const std::string &value, const char *name) {
  std::size_t consumed = 0;
  const int parsed = std::stoi(value, &consumed);
  if (consumed != value.size()) {
    throw std::invalid_argument(std::string(name) + " requires an integer");
  }
  return parsed;
}

Options parse_options(int argc, char **argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string argument(argv[index]);
    if (argument == "--execute") {
      options.execute = true;
      continue;
    }
    if (argument == "--confirm-robot-may-move") {
      options.confirmed = true;
      continue;
    }
    if (index + 1 >= argc) {
      throw std::invalid_argument("missing value for " + argument);
    }
    const std::string value(argv[++index]);
    if (argument == "--id") {
      options.actuator_id = parse_int(value, "--id");
    } else if (argument == "--target-turns") {
      options.target_turns = parse_double(value, "--target-turns");
    } else if (argument == "--expected-start-turns") {
      options.expected_start_turns = parse_double(value, "--expected-start-turns");
    } else if (argument == "--max-start-error-turns") {
      options.max_start_error_turns = parse_double(value, "--max-start-error-turns");
    } else if (argument == "--max-step-turns") {
      options.max_step_turns = parse_double(value, "--max-step-turns");
    } else if (argument == "--profile-max-rpm") {
      options.profile_max_rpm = parse_double(value, "--profile-max-rpm");
    } else if (argument == "--profile-acceleration") {
      options.profile_acceleration = parse_double(value, "--profile-acceleration");
    } else if (argument == "--current-limit-a") {
      options.current_limit_a = parse_double(value, "--current-limit-a");
    } else if (argument == "--current-abort-a") {
      options.current_abort_a = parse_double(value, "--current-abort-a");
    } else if (argument == "--timeout-s") {
      options.timeout_seconds = parse_int(value, "--timeout-s");
    } else if (argument == "--diagnostic-hold-s") {
      options.diagnostic_hold_seconds =
          parse_int(value, "--diagnostic-hold-s");
    } else {
      throw std::invalid_argument("unknown option: " + argument);
    }
  }

  if (options.actuator_id < 1 || options.actuator_id > 255 ||
      options.max_start_error_turns <= 0.0 || options.max_step_turns <= 0.0 ||
      options.profile_max_rpm <= 0.0 || options.profile_max_rpm > 10.0 ||
      options.profile_acceleration <= 0.0 || options.profile_acceleration > 10.0 ||
      options.current_limit_a <= 0.0 || options.current_limit_a > 10.0 ||
      options.current_abort_a < 0.0 ||
      (options.current_abort_a > 0.0 &&
       options.current_abort_a >= options.current_limit_a) ||
      options.timeout_seconds < 1 || options.timeout_seconds > 120 ||
      options.diagnostic_hold_seconds < 0 ||
      options.diagnostic_hold_seconds > 20) {
    throw std::invalid_argument("unsafe or incomplete bounded-step arguments");
  }
  if (options.execute != options.confirmed) {
    throw std::invalid_argument(
        "--execute and --confirm-robot-may-move must be provided together");
  }
  if (options.diagnostic_hold_seconds > 0 &&
      std::abs(options.target_turns - options.expected_start_turns) > 1e-6) {
    throw std::invalid_argument(
        "--diagnostic-hold-s requires target turns equal to expected start turns");
  }
  return options;
}

class EnableGuard {
 public:
  EnableGuard(ActuatorController *controller,
              const ActuatorController::UnifiedID &actuator)
      : controller_(controller), actuator_(actuator) {}

  ~EnableGuard() {
    if (enabled_) {
      const bool ok = controller_->disableActuator(actuator_.actuatorID,
                                                   actuator_.ipAddress);
      std::cerr << "scope_disable,success=" << (ok ? 1 : 0) << '\n';
    }
  }

  bool enable() {
    if (controller_->isEnable(actuator_.actuatorID, actuator_.ipAddress)) {
      return false;
    }
    enabled_ = controller_->enableActuator(actuator_.actuatorID,
                                           actuator_.ipAddress);
    return enabled_;
  }

  bool disable_and_verify() {
    if (!enabled_) {
      return true;
    }
    const bool command_ok = controller_->disableActuator(actuator_.actuatorID,
                                                         actuator_.ipAddress);
    std::this_thread::sleep_for(std::chrono::milliseconds(250));
    const bool still_enabled = controller_->isEnable(actuator_.actuatorID,
                                                      actuator_.ipAddress);
    std::cout << "post_disable_state,id="
              << static_cast<unsigned int>(actuator_.actuatorID)
              << ",enabled=" << (still_enabled ? 1 : 0) << '\n';
    if (!still_enabled) {
      enabled_ = false;
    }
    return command_ok && !still_enabled;
  }

 private:
  ActuatorController *controller_;
  ActuatorController::UnifiedID actuator_;
  bool enabled_ = false;
};

}  // namespace

int main(int argc, char **argv) {
  try {
    const Options options = parse_options(argc, argv);
    const double planned_step = options.target_turns - options.expected_start_turns;
    std::cout << std::fixed << std::setprecision(6)
              << "plan,id=" << options.actuator_id
              << ",expected_start_turns=" << options.expected_start_turns
              << ",target_turns=" << options.target_turns
              << ",planned_step_turns=" << planned_step
              << ",profile_max_rpm=" << options.profile_max_rpm
              << ",profile_acceleration=" << options.profile_acceleration
              << ",current_limit_a=" << options.current_limit_a
              << ",current_abort_a=" << options.current_abort_a
              << ",timeout_s=" << options.timeout_seconds
              << ",diagnostic_hold_s=" << options.diagnostic_hold_seconds << '\n';
    if (std::abs(planned_step) > options.max_step_turns) {
      throw std::invalid_argument("planned step exceeds --max-step-turns");
    }
    if (!options.execute) {
      std::cout << "EXECUTION_DOMAIN=DESKTOP_DRY_RUN\nSAFE_STEP_DRY_RUN_PASS\n";
      return 0;
    }

    std::cout << "EXECUTION_DOMAIN=ROBOT_STATE_CHANGING\n";
    std::signal(SIGINT, handle_signal);
    std::signal(SIGTERM, handle_signal);
    ActuatorController *controller = ActuatorController::initController();
    if (controller == nullptr) {
      throw std::runtime_error("controller initialization returned null");
    }
    Actuator::ErrorsDefine discovery_error = Actuator::ERR_NONE;
    std::vector<ActuatorController::UnifiedID> actuators =
        controller->lookupActuators(discovery_error);
    if (actuators.size() != 6) {
      throw std::runtime_error("expected exactly six discovered actuators");
    }
    for (const auto &actuator : actuators) {
      if (controller->isEnable(actuator.actuatorID, actuator.ipAddress)) {
        throw std::runtime_error("refused because an actuator was already enabled");
      }
    }
    const auto selected = std::find_if(
        actuators.begin(), actuators.end(), [&options](const ActuatorController::UnifiedID &item) {
          return static_cast<int>(item.actuatorID) == options.actuator_id;
        });
    if (selected == actuators.end()) {
      throw std::runtime_error("requested actuator was not discovered");
    }

    EnableGuard guard(controller, *selected);
    if (!guard.enable()) {
      throw std::runtime_error("actuator enable failed");
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(300));
    const std::uint8_t id = selected->actuatorID;
    const std::string &ip = selected->ipAddress;
    const double start = controller->getPosition(id, true, ip);
    const std::uint32_t initial_error = controller->getErrorCode(id, ip);
    std::cout << "measured_start_turns=" << start
              << ",error=0x" << std::hex << initial_error << std::dec << '\n';
    if (initial_error != 0U ||
        std::abs(start - options.expected_start_turns) >
            options.max_start_error_turns ||
        std::abs(options.target_turns - start) > options.max_step_turns) {
      throw std::runtime_error("start state failed safety gate");
    }

    controller->setCurrentLimit(id, options.current_limit_a, ip);
    controller->setProfilePositionAcceleration(id, options.profile_acceleration, ip);
    controller->setProfilePositionDeceleration(id, -options.profile_acceleration, ip);
    controller->setProfilePositionMaxVelocity(id, options.profile_max_rpm, ip);
    const double current_limit = controller->getCurrentLimit(id, true, ip);
    const double acceleration = controller->getProfilePositionAcceleration(id, true, ip);
    const double deceleration = controller->getProfilePositionDeceleration(id, true, ip);
    const double max_velocity = controller->getProfilePositionMaxVelocity(id, true, ip);
    std::cout << "readback,current_limit_a=" << current_limit
              << ",acceleration=" << acceleration
              << ",deceleration=" << deceleration
              << ",max_velocity_rpm=" << max_velocity << '\n';
    if (std::abs(current_limit - options.current_limit_a) > 0.05 ||
        max_velocity > options.profile_max_rpm + 0.1 ||
        acceleration > options.profile_acceleration + 0.1 ||
        deceleration < -options.profile_acceleration - 0.1) {
      throw std::runtime_error("temporary parameter readback failed");
    }
    const std::uint32_t post_parameter_error = controller->getErrorCode(id, ip);
    std::cout << "phase=safety_parameters,error=0x" << std::hex
              << post_parameter_error << std::dec << '\n';
    if (post_parameter_error != 0U) {
      throw std::runtime_error("actuator error after safety parameter writes");
    }

    controller->setPosition(id, start, ip);
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    const double pre_mode_position = controller->getPosition(id, true, ip);
    const std::uint32_t pre_mode_error = controller->getErrorCode(id, ip);
    std::cout << "phase=pre_mode_target,position_turns=" << pre_mode_position
              << ",error=0x" << std::hex << pre_mode_error << std::dec << '\n';
    if (pre_mode_error != 0U || std::abs(pre_mode_position - start) > 0.05) {
      throw std::runtime_error("pre-mode target gate failed");
    }

    controller->activateActuatorMode(id, Actuator::Mode_Profile_Pos, ip);
    controller->setPosition(id, start, ip);
    std::this_thread::sleep_for(std::chrono::milliseconds(300));
    const double hold_position = controller->getPosition(id, true, ip);
    const std::uint32_t post_mode_error = controller->getErrorCode(id, ip);
    std::cout << "phase=profile_mode_hold,position_turns=" << hold_position
              << ",error=0x" << std::hex << post_mode_error << std::dec << '\n';
    if (post_mode_error != 0U ||
        controller->getActuatorMode(id, ip) != Actuator::Mode_Profile_Pos ||
        std::abs(hold_position - start) > 0.05) {
      throw std::runtime_error("profile-position hold gate failed");
    }

    const bool diagnostic_hold = options.diagnostic_hold_seconds > 0;
    const double monitored_target = diagnostic_hold ? start : options.target_turns;
    if (!diagnostic_hold) {
      controller->setPosition(id, options.target_turns, ip);
    }
    const auto deadline = std::chrono::steady_clock::now() +
                          std::chrono::seconds(
                              diagnostic_hold ? options.diagnostic_hold_seconds
                                              : options.timeout_seconds);
    int target_hits = 0;
    int current_hits = 0;
    bool reached = false;
    while (std::chrono::steady_clock::now() < deadline &&
           !stop_requested.load()) {
      const double position = controller->getPosition(id, true, ip);
      const double velocity = controller->getVelocity(id, true, ip);
      const double current = controller->getCurrent(id, true, ip);
      const std::uint32_t error = controller->getErrorCode(id, ip);
      std::cout << (diagnostic_hold ? "hold" : "motion")
                << ",position_turns=" << position
                << ",velocity_rpm=" << velocity
                << ",current_a=" << current
                << ",error=0x" << std::hex << error << std::dec << '\n';
      if (error != 0U) {
        throw std::runtime_error("actuator error during motion");
      }
      if (options.current_abort_a > 0.0) {
        current_hits = std::abs(current) > options.current_abort_a
                           ? current_hits + 1
                           : 0;
        if (current_hits >= 2) {
          throw std::runtime_error("current watchdog triggered");
        }
      }
      if ((diagnostic_hold && std::abs(position - monitored_target) > 0.05) ||
          (!diagnostic_hold && planned_step < 0.0 &&
           position < options.target_turns - 0.05) ||
          (!diagnostic_hold && planned_step > 0.0 &&
           position > options.target_turns + 0.05)) {
        throw std::runtime_error("position overshoot watchdog triggered");
      }
      target_hits = std::abs(position - monitored_target) <= 0.02
                        ? target_hits + 1
                        : 0;
      if (!diagnostic_hold && target_hits >= 3) {
        reached = true;
        break;
      }
      std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
    if (diagnostic_hold && !stop_requested.load() &&
        std::chrono::steady_clock::now() >= deadline) {
      reached = true;
    }
    if (!reached) {
      throw std::runtime_error(stop_requested.load() ? "operator stop" : "motion timeout");
    }
    if (!guard.disable_and_verify()) {
      throw std::runtime_error("post-motion disable verification failed");
    }
    std::cout << (diagnostic_hold ? "SAFE_PROFILE_HOLD_PASS\n"
                                  : "SAFE_STEP_MOVE_PASS\n");
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "SAFE_STEP_MOVE_FAIL: " << error.what() << '\n';
    return 2;
  }
}
