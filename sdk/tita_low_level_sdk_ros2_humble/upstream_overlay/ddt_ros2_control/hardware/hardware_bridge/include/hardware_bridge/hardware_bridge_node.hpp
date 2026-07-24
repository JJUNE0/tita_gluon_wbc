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

#ifndef HARDWARE_BRIDGE__HARDWARE_BRIDGE_NODE_HPP_
#define HARDWARE_BRIDGE__HARDWARE_BRIDGE_NODE_HPP_

#include <algorithm>
#include <chrono>
#include <array>
#include <atomic>
#include <cmath>
#include <limits>
#include <memory>
#include <string>
#include <thread>
#include <vector>

#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/macros.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "tita_robot/tita_robot.hpp"

namespace tita_locomotion
{

struct MotorStatusSummary
{
  size_t nonzero_count{0};
  bool available{false};
  bool all_online{false};
  bool consistent{false};
};

inline MotorStatusSummary summarize_motor_status(
  const std::vector<uint16_t> & status, const size_t expected_count)
{
  MotorStatusSummary summary;
  if (status.size() != expected_count) return summary;
  summary.nonzero_count = static_cast<size_t>(std::count_if(
    status.begin(), status.end(), [](const uint16_t value) {return value != 0U;}));
  summary.available = summary.nonzero_count != 0U;
  summary.all_online = summary.nonzero_count == expected_count;
  // The pinned TITA API leaves this vector at zero until a separate motor-status frame arrives.
  // Direct motor q/dq/effort feedback has its own freshness watchdog, so an entirely unavailable
  // status channel is not interpreted as eight offline motors. A partial status vector is unsafe.
  summary.consistent = !summary.available || summary.all_online;
  return summary;
}

struct Joint
{
  double position = 0.0f;
  double velocity = 0.0f;
  double effort = 0.0f;
  double errorId = 0.0f;

  double effortCommand = 0.0f;
  double positionCommand = 0.0f;
  double velocityCommand = 0.0f;
  double kp = 0.0f;
  double kd = 0.0f;
  double outputLimit = 0.0f;
  std::string name;
};

struct InertiaUnit
{
  std::string name;
  double linear_acceleration[3];
  double angular_velocity[3];
  double orientation[4];  // x y z w
};

class HardwareBridge : public hardware_interface::SystemInterface
{
public:
  HardwareBridge();
  ~HardwareBridge();
  rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn on_init(
    const hardware_interface::HardwareInfo & info) override;
  rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn on_activate(
    const rclcpp_lifecycle::State & /*previous_state*/) override;
  rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn on_deactivate(
    const rclcpp_lifecycle::State & /*previous_state*/) override;

  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;
  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;
  hardware_interface::return_type read(
    const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/) override;
  hardware_interface::return_type write(
    const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/) override;

private:
  static constexpr size_t kLogCapacity = 4096;
  static constexpr size_t kMaxJoints = 8;
  struct WriteLogRecord
  {
    uint64_t monotonic_ns{0};
    uint64_t period_ns{0};
    uint64_t sequence{0};
    double controller_sequence{0.0};
    double stage1_state{0.0};
    double transform_progress{0.0};
    double settle_elapsed{0.0};
    double rl_prepare_elapsed{0.0};
    double rl_blend_alpha{0.0};
    double rl_running_elapsed{0.0};
    double history_valid_count{0.0};
    double inference_ms{0.0};
    bool joy_fresh{false};
    bool joy_zero{false};
    double joy_age_ms{0.0};
    std::array<double, 3> joy_command{};
    double repeated_clipping{0.0};
    double logger_flush_request{0.0};
    bool command_prepared{false};
    bool read_valid{false};
    bool motors_online{false};
    double consecutive_write_failures{0.0};
    std::array<double, kMaxJoints> q{};
    std::array<double, kMaxJoints> v{};
    std::array<double, kMaxJoints> kp{};
    std::array<double, kMaxJoints> kd{};
    std::array<double, kMaxJoints> effort{};
    std::array<double, kMaxJoints> final_torque{};
    std::array<double, kMaxJoints> measured_q{};
    std::array<double, kMaxJoints> measured_v{};
    std::array<double, kMaxJoints> measured_effort{};
    std::array<uint16_t, kMaxJoints> motor_status{};
    std::array<double, 33> observation{};
    std::array<double, kMaxJoints> action_policy{};
    std::array<double, kMaxJoints> action_native{};
    std::array<double, kMaxJoints> action_scaled{};
    std::array<double, kMaxJoints> stand_target{};
    std::array<double, kMaxJoints> rl_target{};
    std::array<double, kMaxJoints> limited_target{};
    std::array<double, kMaxJoints> blended_target{};
    std::array<double, kMaxJoints> clipping_mask{};
    std::array<double, kMaxJoints> joy_axis{};
    std::array<double, 4> imu_quaternion{};
    std::array<double, 3> imu_angular_velocity{};
    std::array<double, 3> imu_linear_acceleration{};
    bool written{false};
  };

  void start_writer_log();
  void stop_writer_log();
  void enqueue_write_log(const WriteLogRecord & record);
  void writer_log_loop();

  // rclcpp::Node::SharedPtr node_;
  // rclcpp::executors::SingleThreadedExecutor executor_;
  std::vector<Joint> mJoints;
  InertiaUnit mImu;
  size_t leg_dof_{4};

private:
  std::unique_ptr<tita_robot> robot_;
  rclcpp::Clock clock_{RCL_SYSTEM_TIME};
  bool pvt_ctrl_{true};
  bool hardware_output_enabled_{false};
  double command_enable_{0.0};
  double stage1_state_command_{0.0};
  double controller_sequence_command_{0.0};
  double transform_progress_command_{0.0};
  double settle_elapsed_command_{0.0};
  double command_prepared_command_{0.0};
  double rl_prepare_elapsed_command_{0.0};
  double rl_blend_alpha_command_{0.0};
  double rl_running_elapsed_command_{0.0};
  double history_valid_count_command_{0.0};
  double inference_ms_command_{0.0};
  double joy_fresh_command_{0.0};
  double joy_zero_command_{0.0};
  double repeated_clipping_command_{0.0};
  double logger_flush_request_command_{0.0};
  double joy_age_ms_command_{0.0};
  std::array<double, 3> joy_command_{};
  std::array<double, 33> observation_command_{};
  std::array<double, kMaxJoints> action_policy_command_{};
  std::array<double, kMaxJoints> action_native_command_{};
  std::array<double, kMaxJoints> action_scaled_command_{};
  std::array<double, kMaxJoints> stand_target_command_{};
  std::array<double, kMaxJoints> rl_target_command_{};
  std::array<double, kMaxJoints> limited_target_command_{};
  std::array<double, kMaxJoints> blended_target_command_{};
  std::array<double, kMaxJoints> clipping_mask_command_{};
  std::array<double, kMaxJoints> joy_axis_command_{};
  double read_valid_{0.0};
  double write_success_{0.0};
  double write_sequence_{0.0};
  double consecutive_write_failures_{0.0};
  double motors_online_{0.0};
  double dropped_write_log_records_{0.0};
  double hardware_output_enabled_state_{0.0};
  double motor_api_write_count_{0.0};
  double imu_fresh_{0.0};
  double motors_fresh_{0.0};
  double joint_vectors_valid_{0.0};
  double state_values_finite_{0.0};
  double motor_status_all_online_{0.0};
  double motor_status_available_{0.0};
  double logger_flushed_sequence_{0.0};
  bool last_reported_read_valid_{false};
  std::array<double, kMaxJoints> last_command_q_{};
  unsigned int write_failure_threshold_{3};
  std::string hardware_log_root_;
  std::array<WriteLogRecord, kLogCapacity> write_log_queue_{};
  std::atomic<size_t> write_log_head_{0};
  std::atomic<size_t> write_log_tail_{0};
  std::atomic<bool> write_log_running_{false};
  std::thread write_log_thread_;
  int write_log_fd_{-1};
  unsigned int logger_fsync_every_records_{250};
  std::atomic<uint64_t> logger_flushed_sequence_atomic_{0};
  std::atomic<bool> write_log_failed_{false};
};
}  // namespace tita_locomotion

#endif  // HARDWARE_BRIDGE__HARDWARE_BRIDGE_NODE_HPP_
