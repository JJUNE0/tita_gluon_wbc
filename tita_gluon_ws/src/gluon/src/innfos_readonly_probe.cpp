#include <cstdint>

#include "actuatorcontroller.h"

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <csignal>
#include <cstdlib>
#include <exception>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

namespace {

std::atomic<bool> stop_requested(false);

struct Options {
  int samples = 1;
  int period_ms = 200;
  int expected_actuators = 6;
  std::vector<int> enable_for_read_ids;
  bool confirm_enable_may_move = false;
  bool disable_all = false;
  bool confirm_disable_may_drop = false;
  int record_all_seconds = 0;
  std::string output_path;
  bool confirm_all_enable_may_move = false;
  int read_controller_config_id = -1;
};

struct SensorSample {
  bool online;
  bool enabled;
  Actuator::ActuatorMode mode;
  std::uint32_t error_code;
  double position_turns;
  double velocity_rpm;
  double current_a;
  double voltage_v;
  double motor_temperature_c;
  double inverter_temperature_c;
};

struct AsyncCvpState {
  std::string ip_address;
  std::uint8_t actuator_id;
  bool current_seen = false;
  bool velocity_seen = false;
  bool position_seen = false;
  double current_a = std::numeric_limits<double>::quiet_NaN();
  double velocity_rpm = std::numeric_limits<double>::quiet_NaN();
  double position_turns = std::numeric_limits<double>::quiet_NaN();
  bool zero_captured = false;
  double zero_turns = std::numeric_limits<double>::quiet_NaN();
  double minimum_turns = std::numeric_limits<double>::infinity();
  double maximum_turns = -std::numeric_limits<double>::infinity();
};

void handle_signal(int) {
  // Deliberately do not disable, enable, or command any actuator here.
  stop_requested.store(true);
}

int parse_nonnegative_int(const std::string &value, const char *option) {
  std::size_t consumed = 0;
  const int parsed = std::stoi(value, &consumed);
  if (consumed != value.size() || parsed < 0) {
    throw std::invalid_argument(std::string(option) + " requires a non-negative integer");
  }
  return parsed;
}

void print_usage(const char *program) {
  std::cout
      << "Usage: " << program
      << " [--samples N] [--period-ms N] [--expected-actuators N]\n"
      << "       [--enable-for-read ID ... --confirm-enable-may-move]\n"
      << "       [--disable-all --confirm-disable-may-drop]\n"
      << "       [--record-all-seconds N --output FILE "
         "--confirm-all-enable-may-move]\n"
      << "       [--read-controller-config ID [--confirm-enable-may-move]]\n"
      << "\n"
      << "Read-only INNFOS Ethernet discovery and sensor probe.\n"
      << "  --samples N              Number of samples (default: 1)\n"
      << "  --period-ms N            Delay between samples (default: 200)\n"
      << "  --expected-actuators N   Expected discovery count; 0 accepts any nonzero count\n"
      << "                           (default: 6)\n"
      << "  --enable-for-read ID     Enable a selected actuator for feedback, then disable it\n"
      << "                           Repeat this option to select multiple actuators\n"
      << "  --confirm-enable-may-move\n"
      << "                           Required acknowledgement for --enable-for-read\n"
      << "  --disable-all            Disable every discovered actuator and exit\n"
      << "  --confirm-disable-may-drop\n"
      << "                           Required acknowledgement for --disable-all\n"
      << "  --record-all-seconds N   Enable all discovered actuators and record CVP at 20 Hz\n"
      << "  --output FILE            CSV path for --record-all-seconds\n"
      << "  --confirm-all-enable-may-move\n"
      << "                           Required acknowledgement for all-actuator enable\n"
      << "  --read-controller-config ID\n"
      << "                           Read loop gains, limits, and profile settings\n"
      << "                           Add --confirm-enable-may-move if refresh requires enable\n";
}

Options parse_options(int argc, char **argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string argument(argv[index]);
    if (argument == "--help" || argument == "-h") {
      print_usage(argv[0]);
      std::exit(0);
    }
    if (argument == "--confirm-enable-may-move") {
      options.confirm_enable_may_move = true;
      continue;
    }
    if (argument == "--disable-all") {
      options.disable_all = true;
      continue;
    }
    if (argument == "--confirm-disable-may-drop") {
      options.confirm_disable_may_drop = true;
      continue;
    }
    if (argument == "--confirm-all-enable-may-move") {
      options.confirm_all_enable_may_move = true;
      continue;
    }
    if (index + 1 >= argc) {
      throw std::invalid_argument("missing value for " + argument);
    }
    const std::string value(argv[++index]);
    if (argument == "--samples") {
      options.samples = parse_nonnegative_int(value, "--samples");
      if (options.samples == 0) {
        throw std::invalid_argument("--samples must be at least 1");
      }
    } else if (argument == "--period-ms") {
      options.period_ms = parse_nonnegative_int(value, "--period-ms");
    } else if (argument == "--expected-actuators") {
      options.expected_actuators = parse_nonnegative_int(value, "--expected-actuators");
    } else if (argument == "--enable-for-read") {
      const int actuator_id = parse_nonnegative_int(value, "--enable-for-read");
      if (actuator_id < 1 || actuator_id > 255) {
        throw std::invalid_argument("--enable-for-read ID must be in [1, 255]");
      }
      if (std::find(options.enable_for_read_ids.begin(),
                    options.enable_for_read_ids.end(), actuator_id) !=
          options.enable_for_read_ids.end()) {
        throw std::invalid_argument("duplicate --enable-for-read ID");
      }
      options.enable_for_read_ids.push_back(actuator_id);
    } else if (argument == "--record-all-seconds") {
      options.record_all_seconds = parse_nonnegative_int(value, "--record-all-seconds");
      if (options.record_all_seconds < 1 || options.record_all_seconds > 600) {
        throw std::invalid_argument("--record-all-seconds must be in [1, 600]");
      }
    } else if (argument == "--output") {
      options.output_path = value;
      if (options.output_path.empty()) {
        throw std::invalid_argument("--output must not be empty");
      }
    } else if (argument == "--read-controller-config") {
      options.read_controller_config_id =
          parse_nonnegative_int(value, "--read-controller-config");
      if (options.read_controller_config_id < 1 ||
          options.read_controller_config_id > 255) {
        throw std::invalid_argument("--read-controller-config ID must be in [1, 255]");
      }
    } else {
      throw std::invalid_argument("unknown option: " + argument);
    }
  }
  if (!options.enable_for_read_ids.empty() && !options.confirm_enable_may_move) {
    throw std::invalid_argument(
        "--enable-for-read requires --confirm-enable-may-move");
  }
  if (options.confirm_enable_may_move && options.enable_for_read_ids.empty() &&
      options.read_controller_config_id < 0) {
    throw std::invalid_argument(
        "--confirm-enable-may-move requires --enable-for-read ID or "
        "--read-controller-config ID");
  }
  if (options.disable_all != options.confirm_disable_may_drop) {
    throw std::invalid_argument(
        "--disable-all requires --confirm-disable-may-drop and vice versa");
  }
  if (options.disable_all && !options.enable_for_read_ids.empty()) {
    throw std::invalid_argument(
        "--disable-all and --enable-for-read are mutually exclusive");
  }
  const bool recording = options.record_all_seconds > 0;
  if (recording != (!options.output_path.empty())) {
    throw std::invalid_argument(
        "--record-all-seconds and --output must be provided together");
  }
  if (recording != options.confirm_all_enable_may_move) {
    throw std::invalid_argument(
        "--record-all-seconds requires --output and --confirm-all-enable-may-move, "
        "and vice versa");
  }
  if (recording && (options.disable_all || !options.enable_for_read_ids.empty())) {
    throw std::invalid_argument(
        "all-actuator recording, --disable-all, and --enable-for-read are mutually exclusive");
  }
  if (options.read_controller_config_id >= 0 &&
      (recording || options.disable_all || !options.enable_for_read_ids.empty())) {
    throw std::invalid_argument(
        "--read-controller-config is mutually exclusive with state-changing modes");
  }
  return options;
}

class SingleActuatorEnableGuard {
 public:
  SingleActuatorEnableGuard(ActuatorController *controller, std::uint8_t actuator_id,
                            const std::string &ip_address)
      : controller_(controller),
        actuator_id_(actuator_id),
        ip_address_(ip_address) {}

  SingleActuatorEnableGuard(const SingleActuatorEnableGuard &) = delete;
  SingleActuatorEnableGuard &operator=(const SingleActuatorEnableGuard &) = delete;

  ~SingleActuatorEnableGuard() {
    if (owns_enable_) {
      const bool disabled = controller_->disableActuator(actuator_id_, ip_address_);
      std::cerr << "emergency_scope_disable,id="
                << static_cast<unsigned int>(actuator_id_)
                << ",success=" << (disabled ? 1 : 0) << '\n';
    }
  }

  bool enable() {
    if (controller_->isEnable(actuator_id_, ip_address_)) {
      std::cerr << "ENABLE_FOR_READ_REFUSED: actuator was already enabled\n";
      return false;
    }
    const bool enabled = controller_->enableActuator(actuator_id_, ip_address_);
    if (!enabled) {
      // The return value may be ambiguous after a communication error. Send a
      // best-effort disable so failure cannot leave an owned enable behind.
      controller_->disableActuator(actuator_id_, ip_address_);
      return false;
    }
    owns_enable_ = true;
    std::cout << "enable_for_read,id=" << static_cast<unsigned int>(actuator_id_)
              << ",success=1\n";
    return true;
  }

  bool disable() {
    if (!owns_enable_) {
      return true;
    }
    const bool disabled = controller_->disableActuator(actuator_id_, ip_address_);
    std::cout << "disable_after_read,id="
              << static_cast<unsigned int>(actuator_id_)
              << ",success=" << (disabled ? 1 : 0) << '\n';
    if (disabled) {
      std::this_thread::sleep_for(std::chrono::milliseconds(200));
      const bool still_enabled = controller_->isEnable(actuator_id_, ip_address_);
      std::cout << "post_disable_state,id="
                << static_cast<unsigned int>(actuator_id_)
                << ",enabled=" << (still_enabled ? 1 : 0) << '\n';
      if (still_enabled) {
        return false;
      }
      owns_enable_ = false;
    }
    return disabled;
  }

 private:
  ActuatorController *controller_;
  std::uint8_t actuator_id_;
  std::string ip_address_;
  bool owns_enable_ = false;
};

class AllActuatorsEnableGuard {
 public:
  AllActuatorsEnableGuard(
      ActuatorController *controller,
      const std::vector<ActuatorController::UnifiedID> &actuators)
      : controller_(controller), actuators_(actuators) {}

  AllActuatorsEnableGuard(const AllActuatorsEnableGuard &) = delete;
  AllActuatorsEnableGuard &operator=(const AllActuatorsEnableGuard &) = delete;

  ~AllActuatorsEnableGuard() {
    if (owns_enable_) {
      const bool disabled = disable_and_verify("emergency_scope_disable_all");
      if (!disabled) {
        std::cerr << "EMERGENCY_SCOPE_DISABLE_ALL_FAIL: physical emergency stop required\n";
      }
    }
  }

  bool enable() {
    for (const auto &actuator : actuators_) {
      if (controller_->isEnable(actuator.actuatorID, actuator.ipAddress)) {
        std::cerr << "ENABLE_ALL_REFUSED: actuator "
                  << static_cast<unsigned int>(actuator.actuatorID)
                  << " was already enabled\n";
        return false;
      }
    }

    const bool aggregate_ok = controller_->enableAllActuators();
    // From this point the aggregate call may have enabled any subset even if
    // its return value is false, so the guard owns cleanup unconditionally.
    owns_enable_ = true;
    std::this_thread::sleep_for(std::chrono::milliseconds(300));
    bool all_enabled = true;
    for (const auto &actuator : actuators_) {
      const bool enabled = controller_->isEnable(actuator.actuatorID,
                                                  actuator.ipAddress);
      all_enabled = all_enabled && enabled;
      std::cout << "post_enable_state,id="
                << static_cast<unsigned int>(actuator.actuatorID)
                << ",enabled=" << (enabled ? 1 : 0) << '\n';
    }
    if (!all_enabled) {
      disable();
      return false;
    }
    if (!aggregate_ok) {
      std::cerr << "ENABLE_ALL_SUSPICIOUS: aggregate SDK return was false, but all "
                   "discovered actuators report enabled\n";
    }
    return true;
  }

  bool disable() {
    if (!owns_enable_) {
      return true;
    }
    const bool disabled = disable_and_verify("disable_after_record_all");
    if (disabled) {
      owns_enable_ = false;
    }
    return disabled;
  }

 private:
  bool disable_and_verify(const char *label) {
    const bool aggregate_ok = controller_->disableAllActuators();
    std::cout << label << ",aggregate_success=" << (aggregate_ok ? 1 : 0) << '\n';
    std::this_thread::sleep_for(std::chrono::milliseconds(300));
    bool any_enabled = false;
    for (const auto &actuator : actuators_) {
      const bool enabled = controller_->isEnable(actuator.actuatorID,
                                                  actuator.ipAddress);
      any_enabled = any_enabled || enabled;
      std::cout << "post_disable_state,id="
                << static_cast<unsigned int>(actuator.actuatorID)
                << ",enabled=" << (enabled ? 1 : 0) << '\n';
    }
    if (!aggregate_ok && !any_enabled) {
      std::cerr << "DISABLE_ALL_SUSPICIOUS: aggregate SDK return was false, but all "
                   "discovered actuators report disabled\n";
    }
    return !any_enabled;
  }

  ActuatorController *controller_;
  std::vector<ActuatorController::UnifiedID> actuators_;
  bool owns_enable_ = false;
};

const char *mode_name(Actuator::ActuatorMode mode) {
  switch (mode) {
    case Actuator::Mode_None:
      return "none";
    case Actuator::Mode_Cur:
      return "current";
    case Actuator::Mode_Vel:
      return "velocity";
    case Actuator::Mode_Pos:
      return "position";
    case Actuator::Mode_Teaching:
      return "teaching";
    case Actuator::Mode_Profile_Pos:
      return "profile_position";
    case Actuator::Mode_Profile_Vel:
      return "profile_velocity";
    case Actuator::Mode_Homing:
      return "homing";
  }
  return "unknown";
}

std::string hex_code(std::uint32_t code) {
  std::ostringstream stream;
  stream << "0x" << std::hex << std::uppercase << code;
  return stream.str();
}

bool all_finite(const SensorSample &sample) {
  return std::isfinite(sample.position_turns) && std::isfinite(sample.velocity_rpm) &&
         std::isfinite(sample.current_a) && std::isfinite(sample.voltage_v) &&
         std::isfinite(sample.motor_temperature_c) &&
         std::isfinite(sample.inverter_temperature_c);
}

bool async_cvp_complete(const AsyncCvpState &state) {
  return state.current_seen && state.velocity_seen && state.position_seen &&
         std::isfinite(state.current_a) && std::isfinite(state.velocity_rpm) &&
         std::isfinite(state.position_turns);
}

SensorSample read_sample(ActuatorController *controller,
                         const ActuatorController::UnifiedID &actuator) {
  const std::uint8_t id = actuator.actuatorID;
  const std::string &ip = actuator.ipAddress;
  return SensorSample{
      controller->isOnline(id, ip),
      controller->isEnable(id, ip),
      controller->getActuatorMode(id, ip),
      controller->getErrorCode(id, ip),
      controller->getPosition(id, true, ip),
      controller->getVelocity(id, true, ip),
      controller->getCurrent(id, true, ip),
      controller->getVoltage(id, true, ip),
      controller->getMotorTemperature(id, true, ip),
      controller->getInverterTemperature(id, true, ip),
  };
}

void print_controller_config(
    ActuatorController *controller,
    const ActuatorController::UnifiedID &actuator) {
  const std::uint8_t id = actuator.actuatorID;
  const std::string &ip = actuator.ipAddress;
  std::cout << std::fixed << std::setprecision(9)
            << "controller_config,ip=" << ip
            << ",id=" << static_cast<unsigned int>(id) << '\n'
            << "position,kp=" << controller->getPositionKp(id, true, ip)
            << ",ki=" << controller->getPositionKi(id, true, ip)
            << ",kd=" << controller->getPositionKd(id, true, ip)
            << ",umax=" << controller->getPositionUmax(id, true, ip)
            << ",umin=" << controller->getPositionUmin(id, true, ip)
            << ",offset=" << controller->getPositionOffset(id, true, ip)
            << ",cutoff_hz=" << controller->getPositionCutoffFrequency(id, true, ip)
            << ",filter_enabled="
            << (controller->isPositionFilterEnable(id, true, ip) ? 1 : 0) << '\n'
            << "position_limits,enabled="
            << (controller->isPositionLimitEnable(id, true, ip) ? 1 : 0)
            << ",minimum_turns=" << controller->getMinimumPosition(id, true, ip)
            << ",maximum_turns=" << controller->getMaximumPosition(id, true, ip)
            << '\n'
            << "profile_position,acceleration="
            << controller->getProfilePositionAcceleration(id, true, ip)
            << ",deceleration="
            << controller->getProfilePositionDeceleration(id, true, ip)
            << ",max_velocity="
            << controller->getProfilePositionMaxVelocity(id, true, ip) << '\n'
            << "velocity,kp=" << controller->getVelocityKp(id, true, ip)
            << ",ki=" << controller->getVelocityKi(id, true, ip)
            << ",umax=" << controller->getVelocityUmax(id, true, ip)
            << ",umin=" << controller->getVelocityUmin(id, true, ip)
            << ",range_rpm=" << controller->getVelocityRange(id, true, ip)
            << ",limit_rpm=" << controller->getVelocityLimit(id, true, ip)
            << ",cutoff_hz=" << controller->getVelocityCutoffFrequency(id, true, ip)
            << ",filter_enabled="
            << (controller->isVelocityFilterEnable(id, true, ip) ? 1 : 0) << '\n'
            << "current,kp=" << controller->getCurrentKp(id, true, ip)
            << ",ki=" << controller->getCurrentKi(id, true, ip)
            << ",range_a=" << controller->getCurrentRange(id, true, ip)
            << ",limit_a=" << controller->getCurrentLimit(id, true, ip)
            << ",cutoff_hz=" << controller->getCurrentCutoffFrequency(id, true, ip)
            << ",filter_enabled="
            << (controller->isCurrentFilterEnable(id, true, ip) ? 1 : 0) << '\n';
}

std::int64_t unix_time_ms() {
  return std::chrono::duration_cast<std::chrono::milliseconds>(
             std::chrono::system_clock::now().time_since_epoch())
      .count();
}

}  // namespace

int main(int argc, char **argv) {
  try {
    const Options options = parse_options(argc, argv);
    std::signal(SIGINT, handle_signal);
    std::signal(SIGTERM, handle_signal);

    if (options.disable_all) {
      std::cout << "EXECUTION_DOMAIN=ROBOT_STATE_CHANGING\n"
                << "DISABLE_GUARD=acknowledged disable-all; arm may drop under gravity\n";
    } else if (options.read_controller_config_id >= 0 &&
               options.confirm_enable_may_move) {
      std::cout << "EXECUTION_DOMAIN=ROBOT_STATE_CHANGING\n"
                << "ENABLE_GUARD=one acknowledged actuator enable for controller "
                   "config refresh; no mode, target, homing, or save API is called\n";
    } else if (options.record_all_seconds > 0) {
      std::cout << "EXECUTION_DOMAIN=ROBOT_STATE_CHANGING\n"
                << "ENABLE_GUARD=acknowledged all-actuator feedback recording; no "
                   "mode, motion, torque, homing, or save API is called\n";
    } else if (!options.enable_for_read_ids.empty()) {
      std::cout << "EXECUTION_DOMAIN=ROBOT_STATE_CHANGING\n"
                << "ENABLE_GUARD=selected acknowledged actuator enables; no mode, motion, "
                   "torque, homing, or save API is called\n";
    } else {
      std::cout << "EXECUTION_DOMAIN=ROBOT_READ_ONLY\n"
                << "READ_ONLY_GUARD=no actuator power enable/disable, mode, command, "
                   "homing, or save API is called\n";
    }

    ActuatorController *controller = ActuatorController::initController();
    if (controller == nullptr) {
      std::cerr << "SENSOR_READ_FAIL: ActuatorController::initController returned null\n";
      return 2;
    }
    std::cout << "sdk_version=" << controller->versionString() << '\n';

    Actuator::ErrorsDefine discovery_error = Actuator::ERR_NONE;
    std::vector<ActuatorController::UnifiedID> actuators =
        controller->lookupActuators(discovery_error);
    std::sort(actuators.begin(), actuators.end(),
              [](const ActuatorController::UnifiedID &left,
                 const ActuatorController::UnifiedID &right) {
                if (left.ipAddress != right.ipAddress) {
                  return left.ipAddress < right.ipAddress;
                }
                return left.actuatorID < right.actuatorID;
              });

    std::cout << "discovery_error="
              << hex_code(static_cast<std::uint32_t>(discovery_error)) << '\n'
              << "discovered_actuators=" << actuators.size() << '\n';
    for (const auto &actuator : actuators) {
      std::cout << "discovered,ip=" << actuator.ipAddress
                << ",id=" << static_cast<unsigned int>(actuator.actuatorID) << '\n';
    }

    if (actuators.empty()) {
      std::cerr << "SENSOR_READ_BLOCKED: no actuator discovered\n";
      return 3;
    }

    if (options.record_all_seconds > 0 &&
        options.expected_actuators != 0 &&
        static_cast<int>(actuators.size()) != options.expected_actuators) {
      std::cerr << "ENABLE_ALL_REFUSED: expected " << options.expected_actuators
                << " actuators, discovered " << actuators.size() << '\n';
      return 5;
    }

    if (options.disable_all) {
      const bool command_ok = controller->disableAllActuators();
      std::cout << "disable_all,success=" << (command_ok ? 1 : 0) << '\n';
      std::this_thread::sleep_for(std::chrono::milliseconds(300));
      bool any_enabled = false;
      for (const auto &actuator : actuators) {
        const bool enabled = controller->isEnable(actuator.actuatorID,
                                                  actuator.ipAddress);
        any_enabled = any_enabled || enabled;
        std::cout << "post_disable_state,id="
                  << static_cast<unsigned int>(actuator.actuatorID)
                  << ",enabled=" << (enabled ? 1 : 0) << '\n';
      }
      if (any_enabled) {
        std::cerr << "DISABLE_ALL_FAIL: operator emergency stop required\n";
        return 5;
      }
      if (!command_ok) {
        std::cerr << "DISABLE_ALL_SUSPICIOUS: aggregate SDK return was false, but "
                     "all discovered actuators report disabled\n";
      }
      std::cout << "DISABLE_ALL_PASS\n";
      return 0;
    }

    if (options.read_controller_config_id >= 0) {
      const auto selected = std::find_if(
          actuators.begin(), actuators.end(), [&options](const ActuatorController::UnifiedID &item) {
            return static_cast<int>(item.actuatorID) ==
                   options.read_controller_config_id;
          });
      if (selected == actuators.end()) {
        std::cerr << "CONTROLLER_CONFIG_BLOCKED: requested actuator ID was not discovered\n";
        return 5;
      }
      std::unique_ptr<SingleActuatorEnableGuard> config_enable_guard;
      if (options.confirm_enable_may_move) {
        config_enable_guard.reset(new SingleActuatorEnableGuard(
            controller, selected->actuatorID, selected->ipAddress));
        if (!config_enable_guard->enable()) {
          std::cerr << "CONTROLLER_CONFIG_BLOCKED: actuator enable failed\n";
          return 5;
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(300));
      }
      std::cout << "controller_state,online="
                << (controller->isOnline(selected->actuatorID, selected->ipAddress) ? 1 : 0)
                << ",enabled="
                << (controller->isEnable(selected->actuatorID, selected->ipAddress) ? 1 : 0)
                << ",mode="
                << mode_name(controller->getActuatorMode(selected->actuatorID,
                                                          selected->ipAddress))
                << ",error="
                << hex_code(controller->getErrorCode(selected->actuatorID,
                                                      selected->ipAddress))
                << '\n';
      print_controller_config(controller, *selected);
      if (config_enable_guard && !config_enable_guard->disable()) {
        std::cerr << "CONTROLLER_CONFIG_DISABLE_FAIL: operator emergency stop required\n";
        return 5;
      }
      std::cout << "CONTROLLER_CONFIG_READ_PASS\n";
      return 0;
    }

    std::ofstream sweep_output;
    if (options.record_all_seconds > 0) {
      sweep_output.open(options.output_path.c_str(),
                        std::ios::out | std::ios::trunc);
      if (!sweep_output.is_open()) {
        std::cerr << "ENABLE_ALL_REFUSED: cannot open output file: "
                  << options.output_path << '\n';
        return 5;
      }
      sweep_output << "time_unix_ms,id,position_turns,delta_turns,velocity_rpm,current_a\n";
      sweep_output.flush();
    }

    std::unique_ptr<AllActuatorsEnableGuard> all_enable_guard;
    if (options.record_all_seconds > 0) {
      all_enable_guard.reset(new AllActuatorsEnableGuard(controller, actuators));
      if (!all_enable_guard->enable()) {
        std::cerr << "ENABLE_ALL_FAIL: initial state or aggregate enable verification failed\n";
        return 5;
      }
    }

    std::vector<std::unique_ptr<SingleActuatorEnableGuard>> enable_guards;
    for (const int requested_id : options.enable_for_read_ids) {
      const auto selected = std::find_if(
          actuators.begin(), actuators.end(), [requested_id](const ActuatorController::UnifiedID &item) {
            return static_cast<int>(item.actuatorID) == requested_id;
          });
      if (selected == actuators.end()) {
        std::cerr << "ENABLE_FOR_READ_REFUSED: requested actuator ID "
                  << requested_id << " was not discovered\n";
        return 5;
      }
      std::unique_ptr<SingleActuatorEnableGuard> guard(new SingleActuatorEnableGuard(
          controller, selected->actuatorID, selected->ipAddress));
      if (!guard->enable()) {
        std::cerr << "ENABLE_FOR_READ_FAIL: actuator " << requested_id
                  << " enable failed\n";
        return 5;
      }
      enable_guards.push_back(std::move(guard));
    }
    if (!enable_guards.empty()) {
      std::this_thread::sleep_for(std::chrono::milliseconds(300));
    }

    bool suspicious = false;
    if (options.expected_actuators != 0 &&
        static_cast<int>(actuators.size()) != options.expected_actuators) {
      std::cerr << "SENSOR_READ_SUSPICIOUS: expected " << options.expected_actuators
                << " actuators, discovered " << actuators.size() << '\n';
      suspicious = true;
    }

    std::vector<AsyncCvpState> async_states;
    async_states.reserve(actuators.size());
    for (const auto &actuator : actuators) {
      AsyncCvpState state;
      state.ip_address = actuator.ipAddress;
      state.actuator_id = actuator.actuatorID;
      async_states.push_back(state);
    }
    controller->addParaRequestCallback(
        [&async_states](ActuatorController::UnifiedID actuator,
                        std::uint8_t parameter_type, double value) {
          const auto state = std::find_if(
              async_states.begin(), async_states.end(),
              [&actuator](const AsyncCvpState &candidate) {
                return candidate.actuator_id == actuator.actuatorID &&
                       candidate.ip_address == actuator.ipAddress;
              });
          if (state == async_states.end()) {
            return;
          }
          switch (parameter_type) {
            case Actuator::ACTUAL_CURRENT:
              state->current_seen = true;
              state->current_a = value;
              break;
            case Actuator::ACTUAL_VELOCITY:
              state->velocity_seen = true;
              state->velocity_rpm = value;
              break;
            case Actuator::ACTUAL_POSITION:
              state->position_seen = true;
              state->position_turns = value;
              if (!state->zero_captured) {
                state->zero_captured = true;
                state->zero_turns = value;
              }
              state->minimum_turns = std::min(state->minimum_turns, value);
              state->maximum_turns = std::max(state->maximum_turns, value);
              break;
            default:
              break;
          }
        });

    // This only starts host-side SDK feedback polling. It does not enable an
    // actuator, select a control mode, or write a motion/torque command.
    for (const auto &actuator : actuators) {
      controller->setAutoRefreshInterval(
          actuator.actuatorID, options.record_all_seconds > 0 ? 50 : 100,
                                         actuator.ipAddress);
      controller->switchAutoRefresh(actuator.actuatorID, true,
                                    actuator.ipAddress);
    }

    // Explicit read requests provide evidence that returned zeros came from a
    // feedback callback rather than only from an uninitialized SDK cache.
    const auto async_deadline = std::chrono::steady_clock::now() +
        (options.record_all_seconds > 0
             ? std::chrono::seconds(options.record_all_seconds)
             : std::chrono::seconds(2));
    auto next_request = std::chrono::steady_clock::now();
    auto next_csv_row = std::chrono::steady_clock::now();
    bool sweep_ready = false;
    while (std::chrono::steady_clock::now() < async_deadline &&
           !stop_requested.load()) {
      const auto now = std::chrono::steady_clock::now();
      if (now >= next_request) {
        for (const auto &actuator : actuators) {
          controller->requestCVPValue(actuator.actuatorID, actuator.ipAddress);
        }
        next_request = now + std::chrono::milliseconds(
                                 options.record_all_seconds > 0 ? 50 : 100);
      }
      ActuatorController::processEvents();

      if (options.record_all_seconds > 0) {
        const bool all_complete = std::all_of(
            async_states.begin(), async_states.end(), async_cvp_complete);
        if (all_complete && !sweep_ready) {
          sweep_ready = true;
          std::cout << "SWEEP_READY: move one joint at a time slowly; stop before "
                       "contact, hard stops, or cable strain\n";
          for (const auto &state : async_states) {
            std::cout << "provisional_zero,id="
                      << static_cast<unsigned int>(state.actuator_id)
                      << ",turns=" << state.zero_turns << '\n';
          }
          std::cout.flush();
        }
        if (sweep_ready && now >= next_csv_row) {
          const std::int64_t timestamp = unix_time_ms();
          sweep_output << std::fixed << std::setprecision(6);
          for (const auto &state : async_states) {
            if (!async_cvp_complete(state)) {
              continue;
            }
            sweep_output << timestamp << ','
                         << static_cast<unsigned int>(state.actuator_id) << ','
                         << state.position_turns << ','
                         << (state.position_turns - state.zero_turns) << ','
                         << state.velocity_rpm << ',' << state.current_a << '\n';
          }
          sweep_output.flush();
          next_csv_row = now + std::chrono::milliseconds(50);
        }
      }
      std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
    for (const auto &actuator : actuators) {
      controller->switchAutoRefresh(actuator.actuatorID, false,
                                    actuator.ipAddress);
    }

    std::cout << "async_cvp,ip,id,current_seen,velocity_seen,position_seen,"
                 "current_a,velocity_rpm,position_turns\n";
    std::cout << std::fixed << std::setprecision(6);
    for (const auto &state : async_states) {
      std::cout << "async_cvp," << state.ip_address << ','
                << static_cast<unsigned int>(state.actuator_id) << ','
                << (state.current_seen ? 1 : 0) << ','
                << (state.velocity_seen ? 1 : 0) << ','
                << (state.position_seen ? 1 : 0) << ',' << state.current_a << ','
                << state.velocity_rpm << ',' << state.position_turns << '\n';
      const bool feedback_expected = options.enable_for_read_ids.empty() ||
          std::find(options.enable_for_read_ids.begin(),
                    options.enable_for_read_ids.end(),
                    static_cast<int>(state.actuator_id)) !=
              options.enable_for_read_ids.end();
      if (feedback_expected && !async_cvp_complete(state)) {
        suspicious = true;
      }
    }

    if (options.record_all_seconds > 0) {
      if (!sweep_ready) {
        suspicious = true;
        std::cerr << "SWEEP_NOT_READY: complete CVP was not received from all actuators\n";
      }
      std::cout << "sweep_summary,id,zero_turns,min_turns,max_turns,min_delta_turns,"
                   "max_delta_turns\n";
      for (const auto &state : async_states) {
        std::cout << "sweep_summary,"
                  << static_cast<unsigned int>(state.actuator_id) << ','
                  << state.zero_turns << ',' << state.minimum_turns << ','
                  << state.maximum_turns << ','
                  << (state.minimum_turns - state.zero_turns) << ','
                  << (state.maximum_turns - state.zero_turns) << '\n';
      }
      std::cout << "sweep_csv=" << options.output_path << '\n';
    }

    std::cout << "sample,time_unix_ms,ip,id,online,enabled,mode,error_code,"
                 "position_turns,velocity_rpm,current_a,voltage_v,motor_temp_c,"
                 "inverter_temp_c\n";
    for (int sample_index = 0;
         sample_index < options.samples && !stop_requested.load(); ++sample_index) {
      for (const auto &actuator : actuators) {
        const SensorSample sample = read_sample(controller, actuator);
        if (!all_finite(sample)) {
          suspicious = true;
        }
        std::cout << sample_index << ',' << unix_time_ms() << ',' << actuator.ipAddress
                  << ',' << static_cast<unsigned int>(actuator.actuatorID) << ','
                  << (sample.online ? 1 : 0) << ',' << (sample.enabled ? 1 : 0) << ','
                  << mode_name(sample.mode) << ',' << hex_code(sample.error_code) << ','
                  << sample.position_turns << ',' << sample.velocity_rpm << ','
                  << sample.current_a << ',' << sample.voltage_v << ','
                  << sample.motor_temperature_c << ','
                  << sample.inverter_temperature_c << '\n';
      }
      std::cout.flush();
      if (sample_index + 1 < options.samples && !stop_requested.load()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(options.period_ms));
      }
    }

    if (all_enable_guard && !all_enable_guard->disable()) {
      std::cerr << "DISABLE_AFTER_RECORD_ALL_FAIL: operator emergency stop required\n";
      return 5;
    }

    bool selected_disable_ok = true;
    for (auto &guard : enable_guards) {
      selected_disable_ok = guard->disable() && selected_disable_ok;
    }
    if (!selected_disable_ok) {
      std::cerr << "DISABLE_AFTER_READ_FAIL: operator emergency stop required\n";
      return 5;
    }

    if (suspicious) {
      std::cerr << "SENSOR_READ_SUSPICIOUS: discovery count or returned values need review\n";
      return 4;
    }
    std::cout << "SENSOR_READ_PASS\n";
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "SENSOR_READ_FAIL: " << error.what() << '\n';
    return 2;
  }
}
