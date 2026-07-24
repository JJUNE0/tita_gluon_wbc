// Copyright (c) 2023 Direct Drive Technology Co., Ltd. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "hardware_bridge/hardware_bridge_node.hpp"

#include <fcntl.h>
#include <pthread.h>
#include <sched.h>
#include <unistd.h>

#include <algorithm>
#include <cctype>
#include <filesystem>
#include <iomanip>
#include <sstream>

#include "pluginlib/class_list_macros.hpp"

namespace tita_locomotion
{
HardwareBridge::HardwareBridge() {}
HardwareBridge::~HardwareBridge()
{
  stop_writer_log();
  // if (direct_mode_) {
  //   std::vector<double> cmd_torque;
  //   cmd_torque.resize(mJoints.size(), 0);
  //   if (!robot_->set_target_joint_t(cmd_torque)) {
  //     RCLCPP_ERROR(
  //       rclcpp::get_logger("hardware_bridge"), "Failed to set target joint torque on exit");
  //   }
  // }
}

rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn HardwareBridge::on_init(
  const hardware_interface::HardwareInfo & info)
{
  if (
    hardware_interface::SystemInterface::on_init(info) !=
    hardware_interface::CallbackReturn::SUCCESS) {
    return hardware_interface::CallbackReturn::ERROR;
  }
  // node_ = rclcpp::Node::make_shared("hardware_bridge_node");
  // executor_.add_node(node_);
  // std::thread([this]() { executor_.spin(); }).detach();
  auto ctrl_mode = info_.hardware_parameters["pvt_ctrl"];
  pvt_ctrl_ = ctrl_mode.compare("false") == 0 ? false : true;
  const auto output_gate = info_.hardware_parameters.find("hardware_output_enabled");
  std::string output_gate_value =
    output_gate == info_.hardware_parameters.end() ? "false" : output_gate->second;
  std::transform(
    output_gate_value.begin(), output_gate_value.end(), output_gate_value.begin(),
    [](const unsigned char value) {return static_cast<char>(std::tolower(value));});
  hardware_output_enabled_ = output_gate_value == "true";
  hardware_output_enabled_state_ = hardware_output_enabled_ ? 1.0 : 0.0;
  const auto threshold = info_.hardware_parameters.find("write_failure_threshold");
  if (threshold != info_.hardware_parameters.end()) {
    write_failure_threshold_ =
      std::max(1U, static_cast<unsigned int>(std::stoul(threshold->second)));
  }
  const auto log_root = info_.hardware_parameters.find("hardware_log_root");
  if (log_root != info_.hardware_parameters.end()) {
    hardware_log_root_ = log_root->second;
  }
  const auto fsync_records = info_.hardware_parameters.find("logger_fsync_every_records");
  if (fsync_records != info_.hardware_parameters.end()) {
    logger_fsync_every_records_ =
      std::max(1U, static_cast<unsigned int>(std::stoul(fsync_records->second)));
  }
  RCLCPP_INFO(rclcpp::get_logger("hardware_bridge"), "Using PVT control: %d", pvt_ctrl_);
  RCLCPP_WARN(
    rclcpp::get_logger("hardware_bridge"), "Hardware motor output gate: %s",
    hardware_output_enabled_ ? "ENABLED" : "DISABLED");
  for (hardware_interface::ComponentInfo component : info.joints) {
    Joint joint;
    joint.name = component.name;
    const auto effort_interface = std::find_if(
      component.command_interfaces.begin(), component.command_interfaces.end(),
      [](const auto & interface) {return interface.name == hardware_interface::HW_IF_EFFORT;});
    if (effort_interface == component.command_interfaces.end() || effort_interface->max.empty()) {
      RCLCPP_ERROR(
        rclcpp::get_logger("hardware_bridge"), "Missing effort max for %s", joint.name.c_str());
      return rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn::ERROR;
    }
    joint.outputLimit = std::stod(effort_interface->max);
    mJoints.push_back(joint);
  }
  for (hardware_interface::ComponentInfo component : info.sensors) {
    if (component.name.find("_imu") != std::string::npos) {
      mImu.name = component.name;
    }
  }

  robot_ = std::make_unique<tita_robot>(mJoints.size());  // depends on urdf
  if (mJoints.size() % 8 == 0)
    leg_dof_ = 4;
  else if (mJoints.size() % 6 == 0)
    leg_dof_ = 3;
  start_writer_log();
  return rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface> HardwareBridge::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> interfaces;
  for (Joint & joint : mJoints) {
    interfaces.emplace_back(
      hardware_interface::StateInterface(
        joint.name, hardware_interface::HW_IF_POSITION, &(joint.position)));
    interfaces.emplace_back(
      hardware_interface::StateInterface(
        joint.name, hardware_interface::HW_IF_VELOCITY, &(joint.velocity)));
    interfaces.emplace_back(
      hardware_interface::StateInterface(
        joint.name, hardware_interface::HW_IF_EFFORT, &(joint.effort)));
  }

  for (hardware_interface::ComponentInfo component : info_.sensors) {
    if (component.name == mImu.name) {
      for (uint i = 0; i < 4; i++) {
        interfaces.emplace_back(
          hardware_interface::StateInterface(
            component.name, component.state_interfaces[i].name, &mImu.orientation[i]));
      }
      for (uint i = 0; i < 3; i++) {
        interfaces.emplace_back(
          hardware_interface::StateInterface(
            component.name, component.state_interfaces[i + 4].name, &mImu.angular_velocity[i]));
      }
      for (uint i = 0; i < 3; i++) {
        interfaces.emplace_back(
          hardware_interface::StateInterface(
            component.name, component.state_interfaces[i + 7].name, &mImu.linear_acceleration[i]));
      }
    }
  }

  interfaces.emplace_back("hardware_bridge", "read_valid", &read_valid_);
  interfaces.emplace_back("hardware_bridge", "write_success", &write_success_);
  interfaces.emplace_back("hardware_bridge", "write_sequence", &write_sequence_);
  interfaces.emplace_back(
    "hardware_bridge", "consecutive_write_failures", &consecutive_write_failures_);
  interfaces.emplace_back("hardware_bridge", "motors_online", &motors_online_);
  interfaces.emplace_back(
    "hardware_bridge", "dropped_write_log_records", &dropped_write_log_records_);
  interfaces.emplace_back(
    "hardware_bridge", "hardware_output_enabled", &hardware_output_enabled_state_);
  interfaces.emplace_back(
    "hardware_bridge", "motor_api_write_count", &motor_api_write_count_);
  interfaces.emplace_back("hardware_bridge", "imu_fresh", &imu_fresh_);
  interfaces.emplace_back("hardware_bridge", "motors_fresh", &motors_fresh_);
  interfaces.emplace_back(
    "hardware_bridge", "joint_vectors_valid", &joint_vectors_valid_);
  interfaces.emplace_back(
    "hardware_bridge", "state_values_finite", &state_values_finite_);
  interfaces.emplace_back(
    "hardware_bridge", "motor_status_all_online", &motor_status_all_online_);
  interfaces.emplace_back(
    "hardware_bridge", "motor_status_available", &motor_status_available_);
  interfaces.emplace_back(
    "hardware_bridge", "logger_flushed_sequence", &logger_flushed_sequence_);
  for (size_t i = 0; i < kMaxJoints; ++i) {
    interfaces.emplace_back(
      "hardware_bridge", "last_command_q" + std::to_string(i), &last_command_q_[i]);
  }

  return interfaces;
}

std::vector<hardware_interface::CommandInterface> HardwareBridge::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> interfaces;
  for (Joint & joint : mJoints) {
    interfaces.emplace_back(
      hardware_interface::CommandInterface(
        joint.name, hardware_interface::HW_IF_POSITION, &(joint.positionCommand)));
    interfaces.emplace_back(
      hardware_interface::CommandInterface(
        joint.name, hardware_interface::HW_IF_VELOCITY, &(joint.velocityCommand)));
    interfaces.emplace_back(
      hardware_interface::CommandInterface(
        joint.name, hardware_interface::HW_IF_EFFORT, &(joint.effortCommand)));
    interfaces.emplace_back(hardware_interface::CommandInterface(joint.name, "kp", &(joint.kp)));
    interfaces.emplace_back(hardware_interface::CommandInterface(joint.name, "kd", &(joint.kd)));
  }
  interfaces.emplace_back("hardware_bridge", "command_enable", &command_enable_);
  interfaces.emplace_back("hardware_bridge", "stage1_state", &stage1_state_command_);
  interfaces.emplace_back(
    "hardware_bridge", "controller_sequence", &controller_sequence_command_);
  interfaces.emplace_back(
    "hardware_bridge", "transform_progress", &transform_progress_command_);
  interfaces.emplace_back("hardware_bridge", "settle_elapsed", &settle_elapsed_command_);
  interfaces.emplace_back("hardware_bridge", "command_prepared", &command_prepared_command_);
  interfaces.emplace_back(
    "hardware_bridge", "rl_prepare_elapsed", &rl_prepare_elapsed_command_);
  interfaces.emplace_back("hardware_bridge", "rl_blend_alpha", &rl_blend_alpha_command_);
  interfaces.emplace_back(
    "hardware_bridge", "rl_running_elapsed", &rl_running_elapsed_command_);
  interfaces.emplace_back(
    "hardware_bridge", "history_valid_count", &history_valid_count_command_);
  interfaces.emplace_back("hardware_bridge", "inference_ms", &inference_ms_command_);
  interfaces.emplace_back("hardware_bridge", "joy_fresh", &joy_fresh_command_);
  interfaces.emplace_back("hardware_bridge", "joy_zero", &joy_zero_command_);
  interfaces.emplace_back(
    "hardware_bridge", "repeated_clipping", &repeated_clipping_command_);
  interfaces.emplace_back(
    "hardware_bridge", "logger_flush_request", &logger_flush_request_command_);
  interfaces.emplace_back("hardware_bridge", "joy_age_ms", &joy_age_ms_command_);
  interfaces.emplace_back("hardware_bridge", "joy_command_vx", &joy_command_[0]);
  interfaces.emplace_back("hardware_bridge", "joy_command_vy", &joy_command_[1]);
  interfaces.emplace_back("hardware_bridge", "joy_command_yaw", &joy_command_[2]);
  for (size_t i = 0; i < observation_command_.size(); ++i) {
    interfaces.emplace_back(
      "hardware_bridge", "obs_current" + std::to_string(i), &observation_command_[i]);
  }
  const auto add_joint_metadata = [&interfaces](
    const std::string & name, std::array<double, kMaxJoints> & values) {
      for (size_t i = 0; i < values.size(); ++i) {
        interfaces.emplace_back("hardware_bridge", name + std::to_string(i), &values[i]);
      }
    };
  add_joint_metadata("action_policy", action_policy_command_);
  add_joint_metadata("action_native", action_native_command_);
  add_joint_metadata("action_scaled", action_scaled_command_);
  add_joint_metadata("stand_target", stand_target_command_);
  add_joint_metadata("rl_target", rl_target_command_);
  add_joint_metadata("limited_target", limited_target_command_);
  add_joint_metadata("blended_target", blended_target_command_);
  add_joint_metadata("clipping_mask", clipping_mask_command_);
  add_joint_metadata("joy_axis", joy_axis_command_);
  return interfaces;
}

rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn
HardwareBridge::on_activate(const rclcpp_lifecycle::State & /*previous_state*/)
{
  command_enable_ = 0.0;
  write_success_ = 0.0;
  consecutive_write_failures_ = 0.0;
  return rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn::SUCCESS;
}

rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn
HardwareBridge::on_deactivate(const rclcpp_lifecycle::State & /*previous_state*/)
{
  return rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn::SUCCESS;
}

hardware_interface::return_type HardwareBridge::read(
  const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
  if (write_log_failed_.load(std::memory_order_acquire)) {
    dropped_write_log_records_ = std::max(dropped_write_log_records_, 1.0);
  }
  logger_flushed_sequence_ = static_cast<double>(
    logger_flushed_sequence_atomic_.load(std::memory_order_acquire));
  const bool imu_timeout = robot_->imu_data_timeout();
  const bool motors_timeout = robot_->motors_data_timeout();
  imu_fresh_ = imu_timeout ? 0.0 : 1.0;
  motors_fresh_ = motors_timeout ? 0.0 : 1.0;
  if (imu_timeout) {
    RCLCPP_WARN_THROTTLE(
      rclcpp::get_logger("hardware_bridge"), clock_, 10000,
      "Imu data read timeout, waiting for connect");

  } else if (motors_timeout) {
    RCLCPP_WARN_THROTTLE(
      rclcpp::get_logger("hardware_bridge"), clock_, 10000,
      "Motors data read timeout, waiting for connect");
  }

  // read from can bus
  auto q = robot_->get_joint_q();
  auto v = robot_->get_joint_v();
  auto t = robot_->get_joint_t();
  auto status = robot_->get_joint_status();
  const bool vectors_invalid =
    q.size() != mJoints.size() || v.size() != mJoints.size() || t.size() != mJoints.size() ||
    status.size() != mJoints.size();
  joint_vectors_valid_ = vectors_invalid ? 0.0 : 1.0;
  if (vectors_invalid) {
    read_valid_ = 0.0;
    motors_online_ = 0.0;
    state_values_finite_ = 0.0;
    motor_status_all_online_ = 0.0;
    motor_status_available_ = 0.0;
    last_reported_read_valid_ = false;
    RCLCPP_WARN_THROTTLE(
      rclcpp::get_logger("hardware_bridge"), clock_, 1000,
      "Direct state invalid: q=%zu v=%zu effort=%zu status=%zu expected=%zu "
      "imu_fresh=%d motors_fresh=%d",
      q.size(), v.size(), t.size(), status.size(), mJoints.size(),
      imu_fresh_ >= 0.5, motors_fresh_ >= 0.5);
    return hardware_interface::return_type::ERROR;
  }
  bool finite = true;
  bool joint_values_finite = true;
  const auto motor_status = summarize_motor_status(status, mJoints.size());
  for (size_t id = 0; id < mJoints.size(); id++) {
    mJoints[id].position = q[id];
    mJoints[id].velocity = v[id];
    mJoints[id].effort = t[id];
    if (id % leg_dof_ == 1) {
      if (mJoints[id].position < -2.5) {
        mJoints[id].position += 2 * M_PI;
      }
    }
    mJoints[id].errorId = status[id];
    const bool joint_finite =
      std::isfinite(q[id]) && std::isfinite(v[id]) && std::isfinite(t[id]);
    joint_values_finite = joint_values_finite && joint_finite;
    finite = finite && joint_finite;
  }
  auto quat = robot_->get_imu_quaternion();
  auto accl = robot_->get_imu_acceleration();
  auto gyro = robot_->get_imu_angular_velocity();

  for (size_t id = 0; id < 3; id++) {
    mImu.linear_acceleration[id] = accl[id];
    mImu.angular_velocity[id] = gyro[id];
    mImu.orientation[id] = quat[id];
  }

  mImu.orientation[3] = quat[3];
  for (const auto value : quat) finite = finite && std::isfinite(value);
  for (const auto value : accl) finite = finite && std::isfinite(value);
  for (const auto value : gyro) finite = finite && std::isfinite(value);
  state_values_finite_ = finite ? 1.0 : 0.0;
  motor_status_available_ = motor_status.available ? 1.0 : 0.0;
  motor_status_all_online_ = motor_status.all_online ? 1.0 : 0.0;
  motors_online_ = joint_values_finite && !motors_timeout && motor_status.consistent ? 1.0 : 0.0;
  read_valid_ = finite && !imu_timeout && !motors_timeout ? 1.0 : 0.0;
  if (!motor_status.available && !motors_timeout && joint_values_finite) {
    RCLCPP_WARN_THROTTLE(
      rclcpp::get_logger("hardware_bridge"), clock_, 10000,
      "Direct motor-status frames unavailable (nonzero=%zu/%zu); using fresh finite "
      "eight-motor q/dq/effort feedback and motor timeout watchdog",
      motor_status.nonzero_count, mJoints.size());
  } else if (motor_status.available && !motor_status.all_online) {
    RCLCPP_ERROR_THROTTLE(
      rclcpp::get_logger("hardware_bridge"), clock_, 1000,
      "Partial motor-status vector is unsafe: nonzero=%zu/%zu",
      motor_status.nonzero_count, mJoints.size());
  }
  const bool read_valid = read_valid_ >= 0.5;
  if (!read_valid) {
    RCLCPP_WARN_THROTTLE(
      rclcpp::get_logger("hardware_bridge"), clock_, 1000,
      "Direct state waiting: read_valid=%d motors_online=%d imu_fresh=%d motors_fresh=%d "
      "vectors_valid=%d finite=%d status_available=%d status_online=%d",
      read_valid, motors_online_ >= 0.5, imu_fresh_ >= 0.5, motors_fresh_ >= 0.5,
      joint_vectors_valid_ >= 0.5, state_values_finite_ >= 0.5,
      motor_status_available_ >= 0.5,
      motor_status_all_online_ >= 0.5);
  } else if (!last_reported_read_valid_) {
    RCLCPP_INFO(
      rclcpp::get_logger("hardware_bridge"),
      "First valid Direct hardware state: eight joints, IMU and motor feedback are fresh; "
      "motor_status_available=%d all_status_flags_online=%d",
      motor_status_available_ >= 0.5, motor_status_all_online_ >= 0.5);
  }
  last_reported_read_valid_ = read_valid;
  return hardware_interface::return_type::OK;
}

hardware_interface::return_type HardwareBridge::write(
  const rclcpp::Time & /*time*/, const rclcpp::Duration & period)
{
  if (!hardware_output_enabled_ || command_enable_ < 0.5) {
    write_success_ = 0.0;
    return hardware_interface::return_type::OK;
  }
  std::vector<double> kp, kd, p, v, t, only_ts;
  WriteLogRecord record;
  record.monotonic_ns = static_cast<uint64_t>(
    std::chrono::duration_cast<std::chrono::nanoseconds>(
      std::chrono::steady_clock::now().time_since_epoch()).count());
  record.period_ns = static_cast<uint64_t>(std::max<int64_t>(period.nanoseconds(), 0));
  record.sequence = static_cast<uint64_t>(write_sequence_) + 1U;
  record.controller_sequence = controller_sequence_command_;
  record.stage1_state = stage1_state_command_;
  record.transform_progress = transform_progress_command_;
  record.settle_elapsed = settle_elapsed_command_;
  record.rl_prepare_elapsed = rl_prepare_elapsed_command_;
  record.rl_blend_alpha = rl_blend_alpha_command_;
  record.rl_running_elapsed = rl_running_elapsed_command_;
  record.history_valid_count = history_valid_count_command_;
  record.inference_ms = inference_ms_command_;
  record.joy_fresh = joy_fresh_command_ >= 0.5;
  record.joy_zero = joy_zero_command_ >= 0.5;
  record.joy_age_ms = joy_age_ms_command_;
  record.joy_command = joy_command_;
  record.repeated_clipping = repeated_clipping_command_;
  record.logger_flush_request = logger_flush_request_command_;
  record.command_prepared = command_prepared_command_ >= 0.5;
  record.read_valid = read_valid_ >= 0.5;
  record.motors_online = motors_online_ >= 0.5;
  record.consecutive_write_failures = consecutive_write_failures_;
  bool finite = mJoints.size() == kMaxJoints;
  for (size_t id = 0; id < mJoints.size(); id++) {
    kp.push_back(mJoints[id].kp);
    kd.push_back(mJoints[id].kd);
    if (id % leg_dof_ == 1 && mJoints[id].positionCommand > M_PI) {
      mJoints[id].positionCommand -= 2 * M_PI;
    }
    p.push_back(mJoints[id].positionCommand);
    if (id < kMaxJoints) last_command_q_[id] = p.back();
    v.push_back(mJoints[id].velocityCommand);
    t.push_back(mJoints[id].effortCommand);
    auto only_t = mJoints[id].effortCommand +
                  mJoints[id].kp * (mJoints[id].positionCommand - mJoints[id].position) +
                  mJoints[id].kd * (mJoints[id].velocityCommand - mJoints[id].velocity);
    only_t = std::clamp(only_t, -mJoints[id].outputLimit, mJoints[id].outputLimit);
    only_ts.push_back(only_t);
    finite = finite && std::isfinite(p.back()) && std::isfinite(v.back()) &&
      std::isfinite(kp.back()) && std::isfinite(kd.back()) && std::isfinite(t.back()) &&
      std::isfinite(only_t);
    if (id < kMaxJoints) {
      record.q[id] = p.back();
      record.v[id] = v.back();
      record.kp[id] = kp.back();
      record.kd[id] = kd.back();
      record.effort[id] = t.back();
      record.final_torque[id] = only_t;
      record.measured_q[id] = mJoints[id].position;
      record.measured_v[id] = mJoints[id].velocity;
      record.measured_effort[id] = mJoints[id].effort;
      record.motor_status[id] = static_cast<uint16_t>(mJoints[id].errorId);
    }
  }
  std::copy(
    std::begin(mImu.orientation), std::end(mImu.orientation),
    record.imu_quaternion.begin());
  std::copy(
    std::begin(mImu.angular_velocity), std::end(mImu.angular_velocity),
    record.imu_angular_velocity.begin());
  std::copy(
    std::begin(mImu.linear_acceleration), std::end(mImu.linear_acceleration),
    record.imu_linear_acceleration.begin());
  std::copy(observation_command_.begin(), observation_command_.end(), record.observation.begin());
  std::copy(
    action_policy_command_.begin(), action_policy_command_.end(), record.action_policy.begin());
  std::copy(
    action_native_command_.begin(), action_native_command_.end(), record.action_native.begin());
  std::copy(
    action_scaled_command_.begin(), action_scaled_command_.end(), record.action_scaled.begin());
  std::copy(
    stand_target_command_.begin(), stand_target_command_.end(), record.stand_target.begin());
  std::copy(rl_target_command_.begin(), rl_target_command_.end(), record.rl_target.begin());
  std::copy(
    limited_target_command_.begin(), limited_target_command_.end(),
    record.limited_target.begin());
  std::copy(
    blended_target_command_.begin(), blended_target_command_.end(),
    record.blended_target.begin());
  std::copy(
    clipping_mask_command_.begin(), clipping_mask_command_.end(),
    record.clipping_mask.begin());
  std::copy(joy_axis_command_.begin(), joy_axis_command_.end(), record.joy_axis.begin());
  bool success = false;
  if (!finite) {
    RCLCPP_ERROR(rclcpp::get_logger("hardware_bridge"), "Rejected non-finite hardware command");
  } else if (pvt_ctrl_) {
    motor_api_write_count_ += 1.0;
    success = robot_->set_target_joint_mit(p, v, kp, kd, t);
    if (!success) {
      RCLCPP_ERROR(rclcpp::get_logger("hardware_bridge"), "Failed to set target PVT on write");
    }
  } else {
    motor_api_write_count_ += 1.0;
    success = robot_->set_target_joint_t(only_ts);
    if (!success) {
      RCLCPP_ERROR(rclcpp::get_logger("hardware_bridge"), "Failed to set target T on write");
    }
  }
  write_sequence_ = static_cast<double>(record.sequence);
  write_success_ = success ? 1.0 : 0.0;
  consecutive_write_failures_ = success ? 0.0 : consecutive_write_failures_ + 1.0;
  record.written = success;
  enqueue_write_log(record);
  if (consecutive_write_failures_ >= static_cast<double>(write_failure_threshold_)) {
    return hardware_interface::return_type::ERROR;
  }
  return hardware_interface::return_type::OK;
}

void HardwareBridge::start_writer_log()
{
  if (hardware_log_root_.empty()) return;
  const auto stamp = std::chrono::duration_cast<std::chrono::seconds>(
    std::chrono::system_clock::now().time_since_epoch()).count();
  const auto directory = std::filesystem::path(hardware_log_root_) /
    ("hardware_session_" + std::to_string(stamp));
  std::filesystem::create_directories(directory);
  const auto path = directory / "hardware_write_log.csv";
  write_log_fd_ = ::open(path.c_str(), O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0644);
  if (write_log_fd_ < 0) return;
  std::ostringstream header;
  header <<
    "monotonic_ns,period_ns,sequence,controller_sequence,stage1_state,transform_progress,"
    "settle_elapsed,rl_prepare_elapsed,rl_blend_alpha,rl_running_elapsed,history_valid_count,"
    "inference_ms,joy_fresh,joy_zero,joy_age_ms,joy_command_vx,joy_command_vy,"
    "joy_command_yaw,repeated_clipping,logger_flush_request,"
    "command_prepared,read_valid,motors_online,consecutive_write_failures,written";
  for (size_t i = 0; i < kMaxJoints; ++i) {
    header << ",q" << i << ",v" << i << ",kp" << i << ",kd" << i
           << ",effort" << i << ",final_torque" << i << ",measured_q" << i
           << ",measured_v" << i << ",measured_effort" << i;
  }
  for (size_t i = 0; i < 4; ++i) header << ",imu_quaternion" << i;
  for (size_t i = 0; i < 3; ++i) header << ",imu_angular_velocity" << i;
  for (size_t i = 0; i < 3; ++i) header << ",imu_linear_acceleration" << i;
  for (size_t i = 0; i < kMaxJoints; ++i) header << ",motor_status" << i;
  for (size_t i = 0; i < 33; ++i) header << ",obs_current" << i;
  for (const auto & prefix : {
      "action_policy", "action_native", "action_scaled", "stand_target", "rl_target",
      "limited_target", "blended_target", "clipping_mask", "joy_axis"})
  {
    for (size_t i = 0; i < kMaxJoints; ++i) header << ',' << prefix << i;
  }
  header << '\n';
  const auto header_line = header.str();
  if (::write(write_log_fd_, header_line.data(), header_line.size()) !=
    static_cast<ssize_t>(header_line.size()))
  {
    ::close(write_log_fd_);
    write_log_fd_ = -1;
    return;
  }
  (void)::fdatasync(write_log_fd_);
  write_log_running_.store(true, std::memory_order_release);
  write_log_thread_ = std::thread(&HardwareBridge::writer_log_loop, this);
}

void HardwareBridge::stop_writer_log()
{
  write_log_running_.store(false, std::memory_order_release);
  if (write_log_thread_.joinable()) write_log_thread_.join();
  if (write_log_fd_ >= 0) {
    (void)::fdatasync(write_log_fd_);
    (void)::close(write_log_fd_);
    write_log_fd_ = -1;
  }
}

void HardwareBridge::enqueue_write_log(const WriteLogRecord & record)
{
  if (!write_log_running_.load(std::memory_order_acquire)) return;
  const size_t head = write_log_head_.load(std::memory_order_relaxed);
  const size_t next = (head + 1U) % kLogCapacity;
  if (next == write_log_tail_.load(std::memory_order_acquire)) {
    dropped_write_log_records_ += 1.0;
    return;
  }
  write_log_queue_[head] = record;
  write_log_head_.store(next, std::memory_order_release);
}

void HardwareBridge::writer_log_loop()
{
  uint64_t written_records = 0;
  while (
    write_log_running_.load(std::memory_order_acquire) ||
    write_log_tail_.load(std::memory_order_acquire) !=
      write_log_head_.load(std::memory_order_acquire)) {
    const size_t tail = write_log_tail_.load(std::memory_order_relaxed);
    if (tail == write_log_head_.load(std::memory_order_acquire)) {
      std::this_thread::sleep_for(std::chrono::milliseconds(2));
      continue;
    }
    const auto & record = write_log_queue_[tail];
    std::ostringstream row;
    row << std::setprecision(17) << record.monotonic_ns << ',' << record.period_ns << ','
        << record.sequence << ',' << record.controller_sequence << ',' << record.stage1_state << ','
        << record.transform_progress << ',' << record.settle_elapsed << ','
        << record.rl_prepare_elapsed << ',' << record.rl_blend_alpha << ','
        << record.rl_running_elapsed << ',' << record.history_valid_count << ','
        << record.inference_ms << ',' << record.joy_fresh << ',' << record.joy_zero << ','
        << record.joy_age_ms << ',' << record.joy_command[0] << ',' << record.joy_command[1] << ','
        << record.joy_command[2] << ','
        << record.repeated_clipping << ',' << record.logger_flush_request << ','
        << record.command_prepared << ',' << record.read_valid << ',' << record.motors_online << ','
        << record.consecutive_write_failures << ',' << record.written;
    for (size_t i = 0; i < kMaxJoints; ++i) {
      row << ',' << record.q[i] << ',' << record.v[i] << ',' << record.kp[i] << ','
          << record.kd[i] << ',' << record.effort[i] << ',' << record.final_torque[i]
          << ',' << record.measured_q[i] << ',' << record.measured_v[i] << ','
          << record.measured_effort[i];
    }
    for (const double value : record.imu_quaternion) row << ',' << value;
    for (const double value : record.imu_angular_velocity) row << ',' << value;
    for (const double value : record.imu_linear_acceleration) row << ',' << value;
    for (const uint16_t value : record.motor_status) row << ',' << value;
    for (const double value : record.observation) row << ',' << value;
    for (const double value : record.action_policy) row << ',' << value;
    for (const double value : record.action_native) row << ',' << value;
    for (const double value : record.action_scaled) row << ',' << value;
    for (const double value : record.stand_target) row << ',' << value;
    for (const double value : record.rl_target) row << ',' << value;
    for (const double value : record.limited_target) row << ',' << value;
    for (const double value : record.blended_target) row << ',' << value;
    for (const double value : record.clipping_mask) row << ',' << value;
    for (const double value : record.joy_axis) row << ',' << value;
    row << '\n';
    const std::string complete_row = row.str();
    size_t offset = 0;
    while (write_log_fd_ >= 0 && offset < complete_row.size()) {
      const ssize_t count = ::write(
        write_log_fd_, complete_row.data() + offset, complete_row.size() - offset);
      if (count <= 0) break;
      offset += static_cast<size_t>(count);
    }
    if (offset != complete_row.size()) {
      // Preserve all earlier complete rows and leave at most one truncated final row for the
      // offline recovery tool. Never append another row behind a partial write.
      write_log_failed_.store(true, std::memory_order_release);
      write_log_running_.store(false, std::memory_order_release);
      write_log_tail_.store(
        write_log_head_.load(std::memory_order_acquire), std::memory_order_release);
      break;
    }
    ++written_records;
    const uint64_t requested_flush = static_cast<uint64_t>(
      std::max(record.logger_flush_request, 0.0));
    const bool explicit_flush = requested_flush >
      logger_flushed_sequence_atomic_.load(std::memory_order_acquire);
    if (write_log_fd_ >= 0 &&
      (explicit_flush || written_records % logger_fsync_every_records_ == 0U))
    {
      if (::fdatasync(write_log_fd_) == 0 && explicit_flush) {
        logger_flushed_sequence_atomic_.store(requested_flush, std::memory_order_release);
      }
    }
    write_log_tail_.store((tail + 1U) % kLogCapacity, std::memory_order_release);
  }
}

}  // namespace tita_locomotion
PLUGINLIB_EXPORT_CLASS(tita_locomotion::HardwareBridge, hardware_interface::SystemInterface)
