#include <cstdint>

#include "actuatorcontroller.h"

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cmath>
#include <csignal>
#include <exception>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

namespace {

const std::size_t kActiveJointCount = 6;
const double kPi = 3.14159265358979323846;
const double kId6BootstrapMaxDeltaTurns = 5.0;
std::atomic<bool> stop_requested(false);

struct JointCalibration {
  int joint_index = 0;
  int actuator_id = -1;
  double gear_ratio = 0.0;
  int direction = 0;
  double zero_turns = std::numeric_limits<double>::quiet_NaN();
  double lower_rad = std::numeric_limits<double>::quiet_NaN();
  double upper_rad = std::numeric_limits<double>::quiet_NaN();
};

struct Options {
  std::string calibration_path =
      "tita_gluon_ws/src/gluon/config/gluon_calibration.yaml";
  std::array<double, kActiveJointCount> target_deg;
  bool target_supplied = false;
  double max_joint_step_deg = 0.0;
  double waypoint_step_deg = 5.0;
  double profile_max_rpm = 0.0;
  double profile_acceleration = 0.0;
  double current_limit_a = 0.0;
  double current_abort_a = 0.0;
  int timeout_seconds = 0;
  int hold_seconds = -1;
  bool hold_until_signal = false;
  bool allow_temporary_position_range_expansion = false;
  bool confirm_high_speed_profile = false;
  bool execute = false;
  bool confirmed = false;
};

struct RuntimeJoint {
  RuntimeJoint(const JointCalibration &calibration_value,
               const ActuatorController::UnifiedID &actuator_value,
               double target_rad_value, double target_turns_value)
      : calibration(calibration_value),
        actuator(actuator_value),
        target_rad(target_rad_value),
        target_turns(target_turns_value) {}

  JointCalibration calibration;
  ActuatorController::UnifiedID actuator;
  double target_rad = 0.0;
  double target_turns = 0.0;
  double start_turns = 0.0;
  int current_hits = 0;
  int target_hits = 0;
};

void handle_signal(int) { stop_requested.store(true); }

std::string trim(const std::string &input) {
  const std::string whitespace = " \t\r\n";
  const std::size_t first = input.find_first_not_of(whitespace);
  if (first == std::string::npos) {
    return "";
  }
  const std::size_t last = input.find_last_not_of(whitespace);
  return input.substr(first, last - first + 1);
}

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
  options.target_deg.fill(0.0);
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
    if (argument == "--hold-until-signal") {
      options.hold_until_signal = true;
      continue;
    }
    if (argument == "--allow-temporary-position-range-expansion") {
      options.allow_temporary_position_range_expansion = true;
      continue;
    }
    if (argument == "--confirm-high-speed-profile") {
      options.confirm_high_speed_profile = true;
      continue;
    }
    if (argument == "--joint-deg") {
      if (index + static_cast<int>(kActiveJointCount) >= argc) {
        throw std::invalid_argument("--joint-deg requires six values");
      }
      for (std::size_t joint = 0; joint < kActiveJointCount; ++joint) {
        options.target_deg[joint] =
            parse_double(argv[++index], "--joint-deg");
      }
      options.target_supplied = true;
      continue;
    }
    if (index + 1 >= argc) {
      throw std::invalid_argument("missing value for " + argument);
    }
    const std::string value(argv[++index]);
    if (argument == "--calibration") {
      options.calibration_path = value;
    } else if (argument == "--max-joint-step-deg") {
      options.max_joint_step_deg = parse_double(value, "--max-joint-step-deg");
    } else if (argument == "--waypoint-step-deg") {
      options.waypoint_step_deg = parse_double(value, "--waypoint-step-deg");
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
    } else if (argument == "--hold-seconds") {
      options.hold_seconds = parse_int(value, "--hold-seconds");
    } else {
      throw std::invalid_argument("unknown option: " + argument);
    }
  }

  if (!options.target_supplied || options.max_joint_step_deg <= 0.0 ||
      options.max_joint_step_deg > 180.0 || options.waypoint_step_deg <= 0.0 ||
      options.waypoint_step_deg > 180.0 || options.profile_max_rpm <= 0.0 ||
      options.profile_max_rpm > 120.0 || options.profile_acceleration <= 0.0 ||
      options.profile_acceleration > 300.0 || options.current_limit_a <= 0.0 ||
      options.current_limit_a > 10.0 || options.current_abort_a < 0.0 ||
      (options.current_abort_a > 0.0 &&
       options.current_abort_a >= options.current_limit_a) ||
      options.timeout_seconds < 1 || options.timeout_seconds > 180 ||
      options.hold_seconds < -1 || options.hold_seconds > 3600 ||
      (options.hold_seconds < 0 && !options.hold_until_signal) ||
      (options.hold_seconds >= 0 && options.hold_until_signal)) {
    throw std::invalid_argument("unsafe or incomplete multi-joint arguments");
  }
  const bool high_speed_profile = options.profile_max_rpm > 10.0 ||
      options.profile_acceleration > 10.0 || options.waypoint_step_deg > 10.0;
  if (high_speed_profile != options.confirm_high_speed_profile) {
    throw std::invalid_argument(
        "high-speed profile values require --confirm-high-speed-profile and vice versa");
  }
  if (options.execute != options.confirmed) {
    throw std::invalid_argument(
        "--execute and --confirm-robot-may-move must be provided together");
  }
  return options;
}

std::array<JointCalibration, kActiveJointCount> load_calibration(
    const std::string &path) {
  std::ifstream input(path.c_str());
  if (!input.is_open()) {
    throw std::runtime_error("cannot open calibration file: " + path);
  }
  std::array<JointCalibration, kActiveJointCount> joints;
  for (std::size_t index = 0; index < joints.size(); ++index) {
    joints[index].joint_index = static_cast<int>(index + 1);
  }

  int active_joint = -1;
  std::string line;
  while (std::getline(input, line)) {
    const std::string value = trim(line);
    if (value.compare(0, 11, "axis_joint_") == 0 &&
        !value.empty() && value[value.size() - 1] == ':') {
      const std::string number = value.substr(11, value.size() - 12);
      const int parsed = parse_int(number, "axis_joint index");
      active_joint = parsed >= 1 && parsed <= 6 ? parsed - 1 : -1;
      continue;
    }
    if (active_joint < 0) {
      continue;
    }
    const std::size_t colon = value.find(':');
    if (colon == std::string::npos) {
      continue;
    }
    const std::string key = trim(value.substr(0, colon));
    const std::string scalar = trim(value.substr(colon + 1));
    JointCalibration &joint = joints[static_cast<std::size_t>(active_joint)];
    if (key == "actuator_id") {
      joint.actuator_id = parse_int(scalar, "actuator_id");
    } else if (key == "gear_ratio") {
      joint.gear_ratio = parse_double(scalar, "gear_ratio");
    } else if (key == "direction") {
      joint.direction = parse_int(scalar, "direction");
    } else if (key == "zero_turns") {
      joint.zero_turns = parse_double(scalar, "zero_turns");
    } else if (key == "urdf_limit_lower_rad") {
      joint.lower_rad = parse_double(scalar, "urdf_limit_lower_rad");
    } else if (key == "urdf_limit_upper_rad") {
      joint.upper_rad = parse_double(scalar, "urdf_limit_upper_rad");
    }
  }

  for (const JointCalibration &joint : joints) {
    if (joint.actuator_id < 1 || joint.actuator_id > 6 ||
        joint.gear_ratio <= 0.0 ||
        (joint.direction != -1 && joint.direction != 1) ||
        !std::isfinite(joint.zero_turns) || !std::isfinite(joint.lower_rad) ||
        !std::isfinite(joint.upper_rad) || joint.lower_rad >= joint.upper_rad) {
      throw std::runtime_error("incomplete active-joint calibration");
    }
  }
  return joints;
}

double joint_rad_to_turns(const JointCalibration &joint, double radians) {
  return joint.zero_turns +
         static_cast<double>(joint.direction) * radians * joint.gear_ratio /
             (2.0 * kPi);
}

double turns_to_joint_rad(const JointCalibration &joint, double turns) {
  return static_cast<double>(joint.direction) * (turns - joint.zero_turns) *
         2.0 * kPi / joint.gear_ratio;
}

class MultiEnableGuard {
 public:
  MultiEnableGuard(ActuatorController *controller,
                   const std::vector<ActuatorController::UnifiedID> &actuators)
      : controller_(controller), actuators_(actuators) {}

  ~MultiEnableGuard() {
    if (owns_enable_) {
      for (const auto &actuator : actuators_) {
        const bool ok = controller_->disableActuator(actuator.actuatorID,
                                                     actuator.ipAddress);
        std::cerr << "scope_disable,id="
                  << static_cast<unsigned int>(actuator.actuatorID)
                  << ",success=" << (ok ? 1 : 0) << '\n';
      }
      std::this_thread::sleep_for(std::chrono::milliseconds(250));
      for (const auto &actuator : actuators_) {
        const bool enabled =
            controller_->isEnable(actuator.actuatorID, actuator.ipAddress);
        std::cerr << "scope_post_disable_state,id="
                  << static_cast<unsigned int>(actuator.actuatorID)
                  << ",enabled=" << (enabled ? 1 : 0) << '\n';
      }
    }
  }

  bool enable_immediate_profile_hold(
      const ActuatorController::UnifiedID &actuator,
      double expected_turns, double current_limit_a,
      double profile_acceleration, double profile_max_rpm) {
    const std::uint8_t id = actuator.actuatorID;
    const std::string &ip = actuator.ipAddress;
    const bool command_ok = controller_->enableActuator(id, ip);
    owns_enable_ = true;
    if (!command_ok) {
      return false;
    }

    // ID6 is an unloaded rotary axis and can spin while an enabled drive is
    // left in its default current mode.  Read it immediately, preload that
    // exact position as the no-step target, and enter Profile Position before
    // enabling the slower-to-bootstrap arm joints.
    const double start_turns = controller_->getPosition(id, true, ip);
    const std::uint32_t initial_error = controller_->getErrorCode(id, ip);
    std::cout << "id6_bootstrap_start,id=" << static_cast<unsigned int>(id)
              << ",turns=" << start_turns
              << ",expected_turns=" << expected_turns
              << ",error=0x" << std::hex << initial_error << std::dec << '\n';
    if (!std::isfinite(start_turns) || initial_error != 0U ||
        std::abs(start_turns - expected_turns) >
            kId6BootstrapMaxDeltaTurns) {
      return false;
    }

    controller_->setPosition(id, start_turns, ip);
    controller_->setCurrentLimit(id, current_limit_a, ip);
    controller_->setProfilePositionAcceleration(id, profile_acceleration, ip);
    controller_->setProfilePositionDeceleration(id, -profile_acceleration, ip);
    controller_->setProfilePositionMaxVelocity(id, profile_max_rpm, ip);
    controller_->activateActuatorMode(id, Actuator::Mode_Profile_Pos, ip);
    controller_->setPosition(id, start_turns, ip);
    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    const double hold_turns = controller_->getPosition(id, true, ip);
    const std::uint32_t hold_error = controller_->getErrorCode(id, ip);
    const bool enabled = controller_->isEnable(id, ip);
    const Actuator::ActuatorMode mode = controller_->getActuatorMode(id, ip);
    std::cout << "id6_bootstrap_hold,id=" << static_cast<unsigned int>(id)
              << ",position_turns=" << hold_turns
              << ",enabled=" << (enabled ? 1 : 0)
              << ",error=0x" << std::hex << hold_error << std::dec << '\n';
    return enabled && mode == Actuator::Mode_Profile_Pos && hold_error == 0U &&
           std::isfinite(hold_turns) &&
           std::abs(hold_turns - start_turns) <= 0.05;
  }

  bool enable_batch_and_verify(
      const std::vector<ActuatorController::UnifiedID> &actuators) {
    const bool command_ok = controller_->enableActuatorInBatch(actuators);
    owns_enable_ = true;
    std::this_thread::sleep_for(std::chrono::milliseconds(300));
    bool all_enabled = true;
    for (const auto &actuator : actuators) {
      const bool enabled =
          controller_->isEnable(actuator.actuatorID, actuator.ipAddress);
      std::cout << "post_enable_state,id="
                << static_cast<unsigned int>(actuator.actuatorID)
                << ",enabled=" << (enabled ? 1 : 0) << '\n';
      all_enabled = all_enabled && enabled;
    }
    std::cout << "batch_enable_command_success=" << (command_ok ? 1 : 0)
              << '\n';
    return command_ok && all_enabled;
  }

  bool disable_and_verify() {
    bool all_disabled = true;
    for (const auto &actuator : actuators_) {
      controller_->disableActuator(actuator.actuatorID, actuator.ipAddress);
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(250));
    for (const auto &actuator : actuators_) {
      const bool enabled =
          controller_->isEnable(actuator.actuatorID, actuator.ipAddress);
      std::cout << "post_disable_state,id="
                << static_cast<unsigned int>(actuator.actuatorID)
                << ",enabled=" << (enabled ? 1 : 0) << '\n';
      all_disabled = all_disabled && !enabled;
    }
    if (all_disabled) {
      owns_enable_ = false;
    }
    return all_disabled;
  }

 private:
  ActuatorController *controller_;
  std::vector<ActuatorController::UnifiedID> actuators_;
  bool owns_enable_ = false;
};

void check_current(RuntimeJoint &joint, double current, double abort_a) {
  if (abort_a <= 0.0) {
    return;
  }
  joint.current_hits = std::abs(current) > abort_a ? joint.current_hits + 1 : 0;
  if (joint.current_hits >= 2) {
    throw std::runtime_error("current watchdog triggered on ID " +
                             std::to_string(joint.calibration.actuator_id));
  }
}

}  // namespace

int main(int argc, char **argv) {
  try {
    const Options options = parse_options(argc, argv);
    const std::array<JointCalibration, kActiveJointCount> calibration =
        load_calibration(options.calibration_path);
    std::array<double, kActiveJointCount> targets_rad;
    std::array<double, kActiveJointCount> targets_turns;
    std::cout << std::fixed << std::setprecision(6);
    for (std::size_t index = 0; index < kActiveJointCount; ++index) {
      targets_rad[index] = options.target_deg[index] * kPi / 180.0;
      if (targets_rad[index] < calibration[index].lower_rad - 1e-9 ||
          targets_rad[index] > calibration[index].upper_rad + 1e-9) {
        throw std::invalid_argument("target violates calibrated URDF limit for joint " +
                                    std::to_string(index + 1));
      }
      targets_turns[index] =
          joint_rad_to_turns(calibration[index], targets_rad[index]);
      std::cout << "plan,joint=" << index + 1
                << ",id=" << calibration[index].actuator_id
                << ",target_deg=" << options.target_deg[index]
                << ",target_turns=" << targets_turns[index]
                << ",lower_deg=" << calibration[index].lower_rad * 180.0 / kPi
                << ",upper_deg=" << calibration[index].upper_rad * 180.0 / kPi
                << '\n';
    }
    std::cout << "plan,profile_max_rpm=" << options.profile_max_rpm
              << ",profile_acceleration=" << options.profile_acceleration
              << ",waypoint_step_deg=" << options.waypoint_step_deg
              << ",current_limit_a=" << options.current_limit_a
              << ",current_abort_a=" << options.current_abort_a
              << ",timeout_s=" << options.timeout_seconds
              << ",temporary_position_range_expansion="
              << (options.allow_temporary_position_range_expansion ? 1 : 0)
              << ",high_speed_profile="
              << (options.confirm_high_speed_profile ? 1 : 0)
              << ",hold="
              << (options.hold_until_signal ? "until_signal"
                                            : std::to_string(options.hold_seconds))
              << '\n';
    if (!options.execute) {
      std::cout << "EXECUTION_DOMAIN=DESKTOP_DRY_RUN\nMULTI_POSE_DRY_RUN_PASS\n";
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
    const std::vector<ActuatorController::UnifiedID> discovered =
        controller->lookupActuators(discovery_error);
    if (discovery_error != Actuator::ERR_NONE || discovered.size() != 6) {
      throw std::runtime_error("expected six actuators with clean discovery");
    }
    for (const auto &actuator : discovered) {
      if (controller->isEnable(actuator.actuatorID, actuator.ipAddress)) {
        throw std::runtime_error("refused because an actuator was already enabled");
      }
    }

    std::vector<ActuatorController::UnifiedID> active_actuators;
    std::vector<RuntimeJoint> joints;
    for (std::size_t index = 0; index < kActiveJointCount; ++index) {
      const auto found = std::find_if(
          discovered.begin(), discovered.end(),
          [&calibration, index](const ActuatorController::UnifiedID &candidate) {
            return static_cast<int>(candidate.actuatorID) ==
                   calibration[index].actuator_id;
          });
      if (found == discovered.end()) {
        throw std::runtime_error("calibrated actuator was not discovered");
      }
      active_actuators.push_back(*found);
      joints.push_back(RuntimeJoint(calibration[index], *found,
                                    targets_rad[index], targets_turns[index]));
    }

    const auto id6_joint = std::find_if(
        joints.begin(), joints.end(), [](const RuntimeJoint &joint) {
          return joint.calibration.actuator_id == 6;
        });
    if (id6_joint == joints.end()) {
      throw std::runtime_error("active ID6 calibration is missing");
    }
    std::vector<ActuatorController::UnifiedID> batch_actuators;
    for (const auto &actuator : active_actuators) {
      if (actuator.actuatorID != 6U) {
        batch_actuators.push_back(actuator);
      }
    }

    MultiEnableGuard guard(controller, active_actuators);
    if (!guard.enable_immediate_profile_hold(
            id6_joint->actuator, id6_joint->calibration.zero_turns,
            options.current_limit_a, options.profile_acceleration,
            options.profile_max_rpm)) {
      throw std::runtime_error("ID6 immediate profile-position bootstrap failed");
    }
    if (!guard.enable_batch_and_verify(batch_actuators)) {
      throw std::runtime_error("ID1-5 batch enable verification failed");
    }

    double largest_step_deg = 0.0;
    for (RuntimeJoint &joint : joints) {
      const std::uint8_t id = joint.actuator.actuatorID;
      const std::string &ip = joint.actuator.ipAddress;
      joint.start_turns = controller->getPosition(id, true, ip);
      const std::uint32_t error = controller->getErrorCode(id, ip);
      const double start_rad =
          turns_to_joint_rad(joint.calibration, joint.start_turns);
      const double step_deg = std::abs(joint.target_rad - start_rad) * 180.0 / kPi;
      largest_step_deg = std::max(largest_step_deg, step_deg);
      std::cout << "start,id=" << static_cast<unsigned int>(id)
                << ",turns=" << joint.start_turns
                << ",joint_deg=" << start_rad * 180.0 / kPi
                << ",step_deg=" << step_deg
                << ",error=0x" << std::hex << error << std::dec << '\n';
      if (error != 0U || step_deg > options.max_joint_step_deg) {
        throw std::runtime_error("initial state gate failed on ID " +
                                 std::to_string(joint.calibration.actuator_id));
      }
      if (options.allow_temporary_position_range_expansion) {
        const double original_minimum =
            controller->getMinimumPosition(id, true, ip);
        const double original_maximum =
            controller->getMaximumPosition(id, true, ip);
        const bool limit_enabled =
            controller->isPositionLimitEnable(id, true, ip);
        const double required_minimum =
            std::min(original_minimum,
                     std::min(joint.start_turns, joint.target_turns) - 0.5);
        const double required_maximum =
            std::max(original_maximum,
                     std::max(joint.start_turns, joint.target_turns) + 0.5);
        if (required_minimum < original_minimum) {
          controller->setMinimumPosition(id, required_minimum, ip);
        }
        if (required_maximum > original_maximum) {
          controller->setMaximumPosition(id, required_maximum, ip);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        const double applied_minimum =
            controller->getMinimumPosition(id, true, ip);
        const double applied_maximum =
            controller->getMaximumPosition(id, true, ip);
        const bool applied_limit_enabled =
            controller->isPositionLimitEnable(id, true, ip);
        std::cout << "temporary_position_range,id="
                  << static_cast<unsigned int>(id)
                  << ",original_min=" << original_minimum
                  << ",original_max=" << original_maximum
                  << ",applied_min=" << applied_minimum
                  << ",applied_max=" << applied_maximum
                  << ",limit_enabled=" << (applied_limit_enabled ? 1 : 0)
                  << '\n';
        if (limit_enabled != applied_limit_enabled ||
            applied_minimum > required_minimum + 0.05 ||
            applied_maximum < required_maximum - 0.05) {
          throw std::runtime_error("temporary position range readback failed on ID " +
                                   std::to_string(joint.calibration.actuator_id));
        }
      }
      controller->setPosition(id, joint.start_turns, ip);
      controller->setCurrentLimit(id, options.current_limit_a, ip);
      controller->setProfilePositionAcceleration(
          id, options.profile_acceleration, ip);
      controller->setProfilePositionDeceleration(
          id, -options.profile_acceleration, ip);
      controller->setProfilePositionMaxVelocity(
          id, options.profile_max_rpm, ip);
    }

    // The bundled SDK examples activate Profile Position one actuator at a
    // time. Initialize and verify each actuator's command cache at its measured
    // position before proceeding to the next axis. The batch mode API can leave
    // some drives reporting ERR_STEP_OVER on their first target update.
    for (const RuntimeJoint &joint : joints) {
      const std::uint8_t id = joint.actuator.actuatorID;
      const std::string &ip = joint.actuator.ipAddress;
      controller->activateActuatorMode(id, Actuator::Mode_Profile_Pos, ip);
      controller->setPosition(id, joint.start_turns, ip);
      std::this_thread::sleep_for(std::chrono::milliseconds(100));
      const double position = controller->getPosition(id, true, ip);
      const std::uint32_t error = controller->getErrorCode(id, ip);
      const Actuator::ActuatorMode mode = controller->getActuatorMode(id, ip);
      std::cout << "mode_gate,id=" << static_cast<unsigned int>(id)
                << ",position_turns=" << position
                << ",error=0x" << std::hex << error << std::dec << '\n';
      if (mode != Actuator::Mode_Profile_Pos || error != 0U ||
          std::abs(position - joint.start_turns) > 0.05) {
        throw std::runtime_error("individual profile-position gate failed on ID " +
                                 std::to_string(joint.calibration.actuator_id));
      }
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(300));
    for (const RuntimeJoint &joint : joints) {
      const std::uint8_t id = joint.actuator.actuatorID;
      const std::string &ip = joint.actuator.ipAddress;
      const double hold_position = controller->getPosition(id, true, ip);
      const std::uint32_t error = controller->getErrorCode(id, ip);
      const double current_limit = controller->getCurrentLimit(id, true, ip);
      const double max_velocity =
          controller->getProfilePositionMaxVelocity(id, true, ip);
      std::cout << "hold_gate,id=" << static_cast<unsigned int>(id)
                << ",position_turns=" << hold_position
                << ",current_limit_a=" << current_limit
                << ",max_velocity_rpm=" << max_velocity
                << ",error=0x" << std::hex << error << std::dec << '\n';
      if (error != 0U ||
          controller->getActuatorMode(id, ip) != Actuator::Mode_Profile_Pos ||
          std::abs(hold_position - joint.start_turns) > 0.05 ||
          std::abs(current_limit - options.current_limit_a) > 0.05 ||
          max_velocity > options.profile_max_rpm + 0.1) {
        throw std::runtime_error("multi-joint hold gate failed on ID " +
                                 std::to_string(joint.calibration.actuator_id));
      }
    }

    const auto motion_deadline = std::chrono::steady_clock::now() +
                                 std::chrono::seconds(options.timeout_seconds);
    const int waypoint_count = std::max(
        1, static_cast<int>(std::ceil(largest_step_deg /
                                      options.waypoint_step_deg)));
    std::cout << "motion_plan,largest_step_deg=" << largest_step_deg
              << ",waypoint_count=" << waypoint_count << '\n';
    bool reached = true;
    int cycle = 0;
    for (int waypoint_index = 1; waypoint_index <= waypoint_count;
         ++waypoint_index) {
      const double fraction = static_cast<double>(waypoint_index) /
                              static_cast<double>(waypoint_count);
      std::cout << "waypoint,index=" << waypoint_index
                << ",count=" << waypoint_count
                << ",fraction=" << fraction << '\n';
      for (RuntimeJoint &joint : joints) {
        joint.target_hits = 0;
        const double waypoint_turns =
            joint.start_turns + fraction * (joint.target_turns - joint.start_turns);
        controller->setPosition(joint.actuator.actuatorID, waypoint_turns,
                                joint.actuator.ipAddress);
      }

      bool waypoint_reached = false;
      while (std::chrono::steady_clock::now() < motion_deadline &&
             !stop_requested.load()) {
        bool all_reached = true;
        for (RuntimeJoint &joint : joints) {
          const std::uint8_t id = joint.actuator.actuatorID;
          const std::string &ip = joint.actuator.ipAddress;
          const double waypoint_turns = joint.start_turns +
              fraction * (joint.target_turns - joint.start_turns);
          const double position = controller->getPosition(id, true, ip);
          const double current = controller->getCurrent(id, true, ip);
          const std::uint32_t error = controller->getErrorCode(id, ip);
          if (cycle % 5 == 0) {
            std::cout << "motion,waypoint=" << waypoint_index
                      << ",id=" << static_cast<unsigned int>(id)
                      << ",position_turns=" << position
                      << ",target_turns=" << waypoint_turns
                      << ",current_a=" << current
                      << ",error=0x" << std::hex << error << std::dec << '\n';
          }
          if (error != 0U) {
            std::cerr << "motion_watchdog_error,waypoint=" << waypoint_index
                      << ",id=" << static_cast<unsigned int>(id)
                      << ",position_turns=" << position
                      << ",target_turns=" << waypoint_turns
                      << ",current_a=" << current
                      << ",error=0x" << std::hex << error << std::dec << '\n';
            throw std::runtime_error("actuator error during multi-joint motion");
          }
          check_current(joint, current, options.current_abort_a);
          const double direction = joint.target_turns - joint.start_turns;
          if ((direction < 0.0 && position < waypoint_turns - 0.05) ||
              (direction > 0.0 && position > waypoint_turns + 0.05)) {
            throw std::runtime_error("position overshoot during multi-joint motion");
          }
          joint.target_hits = std::abs(position - waypoint_turns) <= 0.02
                                  ? joint.target_hits + 1
                                  : 0;
          all_reached = all_reached && joint.target_hits >= 3;
        }
        if (all_reached) {
          waypoint_reached = true;
          std::cout << "waypoint_reached,index=" << waypoint_index
                    << ",count=" << waypoint_count << '\n';
          break;
        }
        ++cycle;
        std::this_thread::sleep_for(std::chrono::milliseconds(20));
      }
      if (!waypoint_reached) {
        reached = false;
        break;
      }
    }
    if (!reached) {
      throw std::runtime_error(stop_requested.load() ? "operator stop during motion"
                                                      : "multi-joint motion timeout");
    }
    std::cout << "MULTI_POSE_REACHED\n";

    const auto hold_deadline = std::chrono::steady_clock::now() +
                               std::chrono::seconds(
                                   options.hold_seconds < 0 ? 0
                                                            : options.hold_seconds);
    cycle = 0;
    while (!stop_requested.load() &&
           (options.hold_until_signal ||
            std::chrono::steady_clock::now() < hold_deadline)) {
      for (RuntimeJoint &joint : joints) {
        const std::uint8_t id = joint.actuator.actuatorID;
        const std::string &ip = joint.actuator.ipAddress;
        const double position = controller->getPosition(id, true, ip);
        const double current = controller->getCurrent(id, true, ip);
        const std::uint32_t error = controller->getErrorCode(id, ip);
        if (cycle % 10 == 0) {
          std::cout << "hold,id=" << static_cast<unsigned int>(id)
                    << ",position_turns=" << position
                    << ",current_a=" << current
                    << ",error=0x" << std::hex << error << std::dec << '\n';
        }
        if (error != 0U || std::abs(position - joint.target_turns) > 0.05) {
          throw std::runtime_error("multi-joint hold watchdog triggered");
        }
        check_current(joint, current, options.current_abort_a);
      }
      ++cycle;
      std::this_thread::sleep_for(std::chrono::milliseconds(20));
    }

    if (!guard.disable_and_verify()) {
      throw std::runtime_error("multi-joint disable verification failed");
    }
    std::cout << (stop_requested.load() ? "MULTI_POSE_OPERATOR_STOP_PASS\n"
                                        : "MULTI_POSE_HOLD_PASS\n");
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "MULTI_POSE_FAIL: " << error.what() << '\n';
    return 2;
  }
}
