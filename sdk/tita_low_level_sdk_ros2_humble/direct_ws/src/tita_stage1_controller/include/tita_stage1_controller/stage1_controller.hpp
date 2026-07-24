#ifndef TITA_STAGE1_CONTROLLER__STAGE1_CONTROLLER_HPP_
#define TITA_STAGE1_CONTROLLER__STAGE1_CONTROLLER_HPP_

#include <atomic>
#include <memory>
#include <optional>
#include <array>
#include <string>
#include <vector>

#include "controller_interface/controller_interface.hpp"
#if __has_include("realtime_tools/realtime_buffer.hpp")
#include "realtime_tools/realtime_buffer.hpp"
#else
#include "realtime_tools/realtime_buffer.h"
#endif
#include "sensor_msgs/msg/joy.hpp"
#include "tita_stage1_controller/rl_pipeline.hpp"
#include "tita_stage1_controller/stage1_core.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_srvs/srv/trigger.hpp"

namespace tita_stage1_controller
{
class Stage1Controller : public controller_interface::ControllerInterface
{
public:
  controller_interface::CallbackReturn on_init() override;
  controller_interface::InterfaceConfiguration command_interface_configuration() const override;
  controller_interface::InterfaceConfiguration state_interface_configuration() const override;
  controller_interface::CallbackReturn on_configure(
    const rclcpp_lifecycle::State &) override;
  controller_interface::CallbackReturn on_activate(
    const rclcpp_lifecycle::State &) override;
  controller_interface::CallbackReturn on_deactivate(
    const rclcpp_lifecycle::State &) override;
  controller_interface::return_type update(
    const rclcpp::Time &, const rclcpp::Duration & period) override;

private:
  struct JoySample
  {
    std::array<float, 8> axes{};
    bool buttons_safe{false};
    bool valid{false};
    int64_t received_steady_ns{0};
  };

  hardware_interface::LoanedCommandInterface * command(
    const std::string & prefix, const std::string & interface);
  const hardware_interface::LoanedStateInterface * state(
    const std::string & prefix, const std::string & interface) const;
  Stage1Config load_config();
  void joy_callback(const sensor_msgs::msg::Joy::SharedPtr message);
  void safe_hold_callback(
    const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
    std::shared_ptr<std_srvs::srv::Trigger::Response> response);
  void update_rl_input(Stage1Input & input, double period_seconds);

  std::vector<std::string> joints_;
  std::vector<hardware_interface::LoanedCommandInterface *> q_cmd_, v_cmd_, effort_cmd_, kp_cmd_, kd_cmd_;
  std::vector<const hardware_interface::LoanedStateInterface *> q_state_, v_state_, effort_state_;
  hardware_interface::LoanedCommandInterface * enable_cmd_{nullptr};
  std::array<hardware_interface::LoanedCommandInterface *, 5> metadata_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, 13> rl_metadata_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kObservationSize> observation_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kJointCount> action_policy_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kJointCount> action_native_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kJointCount> action_scaled_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kJointCount> stand_target_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kJointCount> rl_target_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kJointCount> limited_target_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kJointCount> blended_target_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kJointCount> clipping_mask_cmd_{};
  std::array<hardware_interface::LoanedCommandInterface *, kJointCount> joy_axis_cmd_{};
  std::array<const hardware_interface::LoanedStateInterface *, 10> imu_state_{};
  std::array<const hardware_interface::LoanedStateInterface *, 15> hardware_state_{};
  std::array<const hardware_interface::LoanedStateInterface *, 8> last_command_q_state_{};
  std::unique_ptr<Stage1Core> core_;
  Stage1Config controller_config_{};
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr status_pub_;
  Stage1State last_state_{Stage1State::FAULT};
  bool stage1_only_{true};
  bool stage2_enabled_{false};
  uint64_t controller_sequence_{0};
  uint64_t last_verified_write_sequence_{0};
  JointArray last_prepared_q_{};
  bool last_prepared_valid_{false};
  double command_transport_tolerance_rad_{1e-9};
  bool composite_confirmation_reported_{false};
  bool logger_flush_reported_{false};
  uint64_t logger_flush_request_sequence_{0};
  ObservationBuilder observation_builder_;
  ObservationHistory observation_history_;
  ActionAdapter action_adapter_;
  std::unique_ptr<OnnxPolicyRunner> policy_runner_;
  PolicyStatus policy_status_;
  ObservationArray last_observation_{};
  FloatJointArray last_action_policy_{};
  FloatJointArray previous_action_policy_{};
  FloatJointArray last_action_native_{};
  ActionTargets last_targets_{};
  bool last_inference_valid_{false};
  bool last_observation_valid_{false};
  bool last_target_delta_ok_{false};
  double last_inference_ms_{0.0};
  double policy_elapsed_{0.0};
  double policy_period_seconds_{0.02};
  double max_observed_period_seconds_{0.0};
  uint64_t deadline_miss_count_{0};
  unsigned int repeated_clipping_{0};
  bool rl_prepare_initialized_{false};
  std::string policy_path_;
  std::string policy_sha256_;
  std::string joy_topic_;
  double joy_timeout_seconds_{0.25};
  double joy_zero_tolerance_{0.05};
  std::array<int, 3> joy_command_axes_{2, 0, 3};
  std::array<double, 3> joy_command_signs_{-1.0, 1.0, 1.0};
  std::array<double, 3> joy_command_scales_{3.0, 1.0, 6.0};
  std::array<double, 3> joy_command_limits_{1.0, 0.0, 1.0};
  double joy_command_gain_{0.3};
  std::array<double, 3> joy_speed_ratios_{0.33, 0.66, 1.0};
  int joy_speed_axis_{7};
  int joy_lateral_enable_axis_{5};
  int joy_safe_hold_axis_{4};
  double joy_safe_hold_pressed_max_{-0.5};
  double joy_safe_hold_released_min_{0.5};
  SafeHoldButtonLatch safe_hold_button_latch_;
  FloatJointArray last_joy_axes_{};
  std::array<double, 3> last_joy_command_{};
  double last_joy_age_ms_{1.0e9};
  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_subscription_;
  rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr safe_hold_service_;
  std::atomic_bool safe_hold_requested_{false};
  realtime_tools::RealtimeBuffer<JoySample> joy_buffer_;
};
}  // namespace tita_stage1_controller
#endif
