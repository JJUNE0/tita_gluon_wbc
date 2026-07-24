#include "tita_stage1_controller/stage1_controller.hpp"

#include <algorithm>
#include <cmath>
#include <functional>
#include <chrono>
#include <utility>

#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "pluginlib/class_list_macros.hpp"
#include "rclcpp/version.h"

namespace tita_stage1_controller
{
namespace
{
const std::array<std::string, 5> kCommandInterfaces = {"position", "velocity", "effort", "kp", "kd"};
const std::array<std::string, 5> kMetadataCommandInterfaces = {
  "stage1_state", "controller_sequence", "transform_progress", "settle_elapsed",
  "command_prepared"};
const std::array<std::string, 13> kRlMetadataCommandInterfaces = {
  "rl_prepare_elapsed", "rl_blend_alpha", "rl_running_elapsed", "history_valid_count",
  "inference_ms", "joy_fresh", "joy_zero", "repeated_clipping", "logger_flush_request",
  "joy_age_ms", "joy_command_vx", "joy_command_vy", "joy_command_yaw"};
const std::array<std::string, 3> kJointStateInterfaces = {"position", "velocity", "effort"};
const std::array<std::string, 10> kImuInterfaces = {
  "orientation.x", "orientation.y", "orientation.z", "orientation.w",
  "angular_velocity.x", "angular_velocity.y", "angular_velocity.z",
  "linear_acceleration.x", "linear_acceleration.y", "linear_acceleration.z"};
const std::array<std::string, 15> kHardwareInterfaces = {
  "read_valid", "write_success", "write_sequence", "consecutive_write_failures",
  "motors_online", "dropped_write_log_records", "hardware_output_enabled",
  "motor_api_write_count", "imu_fresh", "motors_fresh", "joint_vectors_valid",
  "state_values_finite", "motor_status_all_online", "motor_status_available",
  "logger_flushed_sequence"};
const std::array<std::string, 8> kLastCommandQInterfaces = {
  "last_command_q0", "last_command_q1", "last_command_q2", "last_command_q3",
  "last_command_q4", "last_command_q5", "last_command_q6", "last_command_q7"};
constexpr std::size_t kPolicyDiagnosticFields = 81U;
constexpr double kEstimatorTargetScale = 2.0;
constexpr double kWheelRadiusM = 0.0925;

bool set_command(hardware_interface::LoanedCommandInterface * interface, const double value)
{
#if RCLCPP_VERSION_MAJOR >= 21
  return interface->set_value(value);
#else
  interface->set_value(value);
  return true;
#endif
}
}  // namespace

controller_interface::CallbackReturn Stage1Controller::on_init()
{
  joints_ = auto_declare<std::vector<std::string>>("joints", {});
  stage1_only_ = auto_declare<bool>("stage1_only", true);
  stage2_enabled_ = auto_declare<bool>("stage2.enabled", false);
  if (stage1_only_ == stage2_enabled_) {
    RCLCPP_ERROR(
      get_node()->get_logger(),
      "Exactly one production mode is required: stage1_only XOR stage2.enabled");
    return controller_interface::CallbackReturn::ERROR;
  }
  try {
    controller_config_ = load_config();
    core_ = std::make_unique<Stage1Core>(controller_config_);
  } catch (const std::exception & error) {
    RCLCPP_ERROR(get_node()->get_logger(), "Invalid Stage 1 parameters: %s", error.what());
    return controller_interface::CallbackReturn::ERROR;
  }
  if (joints_.size() != kJointCount || !core_->valid_config()) {
    RCLCPP_ERROR(get_node()->get_logger(), "Exactly eight joints and a valid official profile are required");
    return controller_interface::CallbackReturn::ERROR;
  }
  if (stage2_enabled_) {
    policy_path_ = auto_declare<std::string>("stage2.policy_path", "");
    policy_sha256_ = auto_declare<std::string>("stage2.policy_sha256", "");
    joy_topic_ = auto_declare<std::string>("stage2.joy_topic", "/tita4252763/joy");
    const double policy_rate_hz = auto_declare<double>("stage2.policy_rate_hz", 50.0);
    joy_timeout_seconds_ = auto_declare<double>("stage2.joy_timeout_seconds", 0.25);
    joy_zero_tolerance_ = auto_declare<double>("stage2.joy_zero_tolerance", 0.05);
    const auto axes = auto_declare<std::vector<int64_t>>(
      "stage2.joy_command_axes", {2, 0, 3});
    const auto signs = auto_declare<std::vector<double>>(
      "stage2.joy_command_signs", {-1.0, 1.0, 1.0});
    const auto scales = auto_declare<std::vector<double>>(
      "stage2.joy_command_scales", {3.0, 1.0, 6.0});
    const auto limits = auto_declare<std::vector<double>>(
      "stage2.joy_command_limits", {1.0, 0.0, 1.0});
    joy_command_gain_ = auto_declare<double>("stage2.joy_command_gain", 0.75);
    joy_command_ramp_rate_ = auto_declare<double>("stage2.joy_command_ramp_rate", 0.5);
    joy_command_stop_seconds_ = auto_declare<double>("stage2.joy_command_stop_seconds", 0.5);
    const auto ratios = auto_declare<std::vector<double>>(
      "stage2.joy_speed_ratios", {0.33, 0.66, 1.0});
    joy_speed_axis_ = auto_declare<int>("stage2.joy_speed_axis", 7);
    joy_lateral_enable_axis_ = auto_declare<int>("stage2.joy_lateral_enable_axis", 5);
    joy_safe_hold_axis_ = auto_declare<int>("stage2.joy_safe_hold_axis", 4);
    joy_safe_hold_pressed_max_ = auto_declare<double>(
      "stage2.joy_safe_hold_pressed_max", -0.5);
    joy_safe_hold_released_min_ = auto_declare<double>(
      "stage2.joy_safe_hold_released_min", 0.5);
    if (policy_path_.empty() || policy_sha256_.size() != 64U ||
      !(policy_rate_hz > 0.0) || axes.size() != 3U || signs.size() != 3U ||
      scales.size() != 3U || limits.size() != 3U || ratios.size() != 3U ||
      !std::isfinite(joy_command_gain_) || joy_command_gain_ <= 0.0 ||
      joy_command_gain_ > 1.0 ||
      !std::isfinite(joy_command_ramp_rate_) || joy_command_ramp_rate_ <= 0.0 ||
      !std::isfinite(joy_command_stop_seconds_) || joy_command_stop_seconds_ <= 0.0 ||
      joy_safe_hold_axis_ < 0 || joy_safe_hold_axis_ >= 8 ||
      !std::isfinite(joy_safe_hold_pressed_max_) ||
      !std::isfinite(joy_safe_hold_released_min_) ||
      joy_safe_hold_pressed_max_ >= joy_safe_hold_released_min_)
    {
      RCLCPP_ERROR(get_node()->get_logger(), "Invalid fixed Stage 2 policy/Joy parameters");
      return controller_interface::CallbackReturn::ERROR;
    }
    policy_period_seconds_ = 1.0 / policy_rate_hz;
    for (std::size_t index = 0; index < 3U; ++index) {
      joy_command_axes_[index] = static_cast<int>(axes[index]);
      joy_command_signs_[index] = signs[index];
      if (!std::isfinite(limits[index]) || limits[index] < 0.0) {
        RCLCPP_ERROR(get_node()->get_logger(), "Invalid Stage 2 Joy command limit");
        return controller_interface::CallbackReturn::ERROR;
      }
      joy_command_limits_[index] = limits[index];
      joy_command_scales_[index] = scales[index];
      joy_speed_ratios_[index] = ratios[index];
    }
    policy_runner_ = std::make_unique<OnnxPolicyRunner>();
    policy_status_ = policy_runner_->load(policy_path_, policy_sha256_, true);
    if (!policy_status_.loaded) {
      RCLCPP_ERROR(
        get_node()->get_logger(), "Stage 2 policy validation failed: %s",
        policy_status_.detail.c_str());
      return controller_interface::CallbackReturn::ERROR;
    }
  }
  return controller_interface::CallbackReturn::SUCCESS;
}

Stage1Config Stage1Controller::load_config()
{
  Stage1Config config;
  const auto array = [this](const std::string & name, const std::vector<double> & defaults) {
      const auto values = auto_declare<std::vector<double>>(name, defaults);
      if (values.size() != kJointCount) throw std::runtime_error(name + " must contain eight values");
      JointArray result{};
      std::copy(values.begin(), values.end(), result.begin());
      return result;
    };
  config.fold_jpos = array("transform_up.fold_jpos", {0.75, 1.2, -2.7, 0.0, -0.75, 1.2, -2.7, 0.0});
  config.stand_jpos = array("transform_up.stand_jpos", {-0.05, 0.9, -2.6, 0.0, 0.05, 0.9, -2.6, 0.0});
  config.transform_kp = array("transform_up.joint_kp", {600, 80, 80, 5, 600, 80, 80, 5});
  config.transform_kd = array("transform_up.joint_kd", {8, 8, 8, 0.5, 8, 8, 8, 0.5});
  config.ff_effort = array("transform_up.ff_torque", {-20, 0, -25, 0, 20, 0, -25, 0});
  config.transition_lower_limits = array(
    "transform_up.transition_lower_limits",
    {-0.785398, -1.919862, -2.7, -62831.85, -0.785398, -1.919862, -2.7, -62831.85});
  config.transition_upper_limits = array(
    "transform_up.transition_upper_limits",
    {0.785398, 3.490659, -0.698132, 62831.85, 0.785398, 3.490659, -0.698132, 62831.85});
  config.lower_limits = array("safety.lower_limits", {-0.785398, -1.919862, -2.670354, -62831.85, -0.785398, -1.919862, -2.670354, -62831.85});
  config.upper_limits = array("safety.upper_limits", {0.785398, 3.490659, -0.698132, 62831.85, 0.785398, 3.490659, -0.698132, 62831.85});
  config.effort_limits = array("safety.effort_limits", {60, 60, 60, 20, 60, 60, 60, 20});
  config.rl_kp = array("stage2.joint_kp", {60, 60, 60, 0, 60, 60, 60, 0});
  config.rl_kd = array("stage2.joint_kd", {1.5, 1.5, 1.5, 0.5, 1.5, 1.5, 1.5, 0.5});
  config.fold_timer = auto_declare<double>("transform_up.fold_timer", 4.0);
  config.stand_timer = auto_declare<double>("transform_up.stand_timer", 2.0);
  config.settle_seconds = auto_declare<double>("settle.seconds", 5.0);
  config.settle_timeout_seconds = auto_declare<double>("settle.timeout_seconds", 10.0);
  config.stand_error_rad = auto_declare<double>("settle.stand_error_rad", 0.15);
  config.wheel_velocity_rad_s = auto_declare<double>("settle.wheel_velocity_rad_s", 0.3);
  config.max_roll_rad = auto_declare<double>("safety.max_roll_rad", 0.35);
  config.max_pitch_rad = auto_declare<double>("safety.max_pitch_rad", 0.35);
  config.fall_tilt_rad = auto_declare<double>("safety.fall_tilt_rad", 0.65);
  config.max_angular_velocity_rad_s = auto_declare<double>("safety.max_angular_velocity_rad_s", 1.5);
  config.max_target_slew_rad_s = auto_declare<double>("safety.max_target_slew_rad_s", 1.5);
  config.max_period_seconds = auto_declare<double>("safety.max_period_seconds", 0.01);
  config.hardware_state_wait_timeout_seconds = auto_declare<double>(
    "safety.hardware_state_wait_timeout_seconds", 1.0);
  config.hardware_state_stable_seconds = auto_declare<double>(
    "safety.hardware_state_stable_seconds", 0.10);
  config.operational_entry_timeout_seconds = auto_declare<double>(
    "safety.operational_entry_timeout_seconds", 2.0);
  config.operational_entry_stable_seconds = auto_declare<double>(
    "safety.operational_entry_stable_seconds", 0.10);
  config.operational_entry_margin_rad = auto_declare<double>(
    "safety.operational_entry_margin_rad", 0.02);
  config.operational_entry_max_joint_velocity_rad_s = auto_declare<double>(
    "safety.operational_entry_max_joint_velocity_rad_s", 0.5);
  config.operational_envelope_tolerance_rad = auto_declare<double>(
    "safety.operational_envelope_tolerance_rad", 1.0e-6);
  command_transport_tolerance_rad_ = auto_declare<double>(
    "safety.command_transport_tolerance_rad", 1e-9);
  if (!std::isfinite(command_transport_tolerance_rad_) ||
    command_transport_tolerance_rad_ < 0.0)
  {
    throw std::runtime_error("safety.command_transport_tolerance_rad must be finite and nonnegative");
  }
  config.write_failure_threshold = static_cast<unsigned int>(
    auto_declare<int>("safety.write_failure_threshold", 3));
  config.stage2_enabled = stage2_enabled_;
  config.rl_running_seconds = auto_declare<double>("stage2.rl_running_seconds", 2.0);
  config.allow_clipped_rl_diagnostic = auto_declare<bool>(
    "stage2.allow_clipped_rl_diagnostic", false);
  config.require_zero_joystick = auto_declare<bool>("stage2.require_zero_joystick", true);
  config.max_leg_target_delta_rad = auto_declare<double>(
    "stage2.max_leg_target_delta_rad", 0.25);
  config.max_leg_target_slew_rad_s = auto_declare<double>(
    "stage2.max_leg_target_slew_rad_s", 0.5);
  config.max_wheel_velocity_rad_s = auto_declare<double>(
    "stage2.max_wheel_velocity_rad_s", 5.0);
  config.max_wheel_accel_rad_s = auto_declare<double>(
    "stage2.max_wheel_accel_rad_s", 5.0);
  config.max_inference_seconds = auto_declare<double>(
    "stage2.max_inference_seconds", 0.010);
  config.max_repeated_clipping = static_cast<unsigned int>(
    auto_declare<int>("stage2.max_repeated_clipping", 5));
  return config;
}

controller_interface::InterfaceConfiguration Stage1Controller::command_interface_configuration() const
{
  std::vector<std::string> names;
  for (const auto & joint : joints_) for (const auto & interface : kCommandInterfaces) names.push_back(joint + "/" + interface);
  names.push_back("hardware_bridge/command_enable");
  for (const auto & interface : kMetadataCommandInterfaces) {
    names.push_back("hardware_bridge/" + interface);
  }
  for (const auto & interface : kRlMetadataCommandInterfaces) {
    names.push_back("hardware_bridge/" + interface);
  }
  for (std::size_t index = 0; index < kObservationSize; ++index) {
    names.push_back("hardware_bridge/obs_current" + std::to_string(index));
  }
  for (const auto & prefix : {
      "action_policy", "action_native", "action_scaled", "stand_target", "rl_target",
      "limited_target", "blended_target", "clipping_mask", "joy_axis"})
  {
    for (std::size_t index = 0; index < kJointCount; ++index) {
      names.push_back("hardware_bridge/" + std::string(prefix) + std::to_string(index));
    }
  }
  return {controller_interface::interface_configuration_type::INDIVIDUAL, names};
}

controller_interface::InterfaceConfiguration Stage1Controller::state_interface_configuration() const
{
  std::vector<std::string> names;
  for (const auto & joint : joints_) for (const auto & interface : kJointStateInterfaces) names.push_back(joint + "/" + interface);
  for (const auto & interface : kImuInterfaces) names.push_back("trunk_imu/" + interface);
  for (const auto & interface : kHardwareInterfaces) names.push_back("hardware_bridge/" + interface);
  for (const auto & interface : kLastCommandQInterfaces) {
    names.push_back("hardware_bridge/" + interface);
  }
  return {controller_interface::interface_configuration_type::INDIVIDUAL, names};
}

controller_interface::CallbackReturn Stage1Controller::on_configure(const rclcpp_lifecycle::State &)
{
  status_pub_ = get_node()->create_publisher<std_msgs::msg::String>("~/stage1_status", 10);
  diagnostic_publisher_ = get_node()->create_publisher<std_msgs::msg::Float64MultiArray>(
    "~/policy_diagnostics", rclcpp::SensorDataQoS());
  realtime_diagnostic_publisher_ =
    std::make_shared<realtime_tools::RealtimePublisher<std_msgs::msg::Float64MultiArray>>(
    diagnostic_publisher_);
  realtime_diagnostic_publisher_->msg_.data.resize(kPolicyDiagnosticFields, 0.0);
  safe_hold_service_ = get_node()->create_service<std_srvs::srv::Trigger>(
    "~/request_safe_hold",
    std::bind(
      &Stage1Controller::safe_hold_callback, this,
      std::placeholders::_1, std::placeholders::_2));
  if (stage2_enabled_) {
    joy_subscription_ = get_node()->create_subscription<sensor_msgs::msg::Joy>(
      joy_topic_, rclcpp::SensorDataQoS(),
      std::bind(&Stage1Controller::joy_callback, this, std::placeholders::_1));
  }
  return controller_interface::CallbackReturn::SUCCESS;
}

void Stage1Controller::safe_hold_callback(
  const std::shared_ptr<std_srvs::srv::Trigger::Request>,
  std::shared_ptr<std_srvs::srv::Trigger::Response> response)
{
  safe_hold_requested_.store(true, std::memory_order_release);
  response->success = true;
  response->message = "SAFE_HOLD requested; confirm controller status before power removal";
}

void Stage1Controller::joy_callback(const sensor_msgs::msg::Joy::SharedPtr message)
{
  JoySample sample;
  if (message->axes.size() < sample.axes.size()) {
    joy_buffer_.writeFromNonRT(sample);
    return;
  }
  sample.valid = true;
  for (std::size_t index = 0; index < sample.axes.size(); ++index) {
    sample.axes[index] = message->axes[index];
    sample.valid = sample.valid && std::isfinite(sample.axes[index]);
  }
  sample.buttons_safe = std::all_of(
    message->buttons.begin(), message->buttons.end(), [](const int32_t value) {return value == 0;});
  sample.received_steady_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(
    std::chrono::steady_clock::now().time_since_epoch()).count();
  joy_buffer_.writeFromNonRT(sample);
}

hardware_interface::LoanedCommandInterface * Stage1Controller::command(
  const std::string & prefix, const std::string & interface)
{
  const auto found = std::find_if(command_interfaces_.begin(), command_interfaces_.end(),
    [&](auto & item) {return item.get_prefix_name() == prefix && item.get_interface_name() == interface;});
  return found == command_interfaces_.end() ? nullptr : &(*found);
}

const hardware_interface::LoanedStateInterface * Stage1Controller::state(
  const std::string & prefix, const std::string & interface) const
{
  const auto found = std::find_if(state_interfaces_.begin(), state_interfaces_.end(),
    [&](const auto & item) {return item.get_prefix_name() == prefix && item.get_interface_name() == interface;});
  return found == state_interfaces_.end() ? nullptr : &(*found);
}

controller_interface::CallbackReturn Stage1Controller::on_activate(const rclcpp_lifecycle::State &)
{
  if (!core_->command_envelopes_valid()) {
    RCLCPP_ERROR(
      get_node()->get_logger(),
      "Stage 1 activation blocked: transition/operational envelopes are invalid");
    return controller_interface::CallbackReturn::ERROR;
  }
  q_cmd_.clear(); v_cmd_.clear(); effort_cmd_.clear(); kp_cmd_.clear(); kd_cmd_.clear();
  q_state_.clear(); v_state_.clear(); effort_state_.clear();
  for (const auto & joint : joints_) {
    q_cmd_.push_back(command(joint, "position")); v_cmd_.push_back(command(joint, "velocity"));
    effort_cmd_.push_back(command(joint, "effort")); kp_cmd_.push_back(command(joint, "kp"));
    kd_cmd_.push_back(command(joint, "kd")); q_state_.push_back(state(joint, "position"));
    v_state_.push_back(state(joint, "velocity")); effort_state_.push_back(state(joint, "effort"));
  }
  enable_cmd_ = command("hardware_bridge", "command_enable");
  for (std::size_t i = 0; i < kMetadataCommandInterfaces.size(); ++i) {
    metadata_cmd_[i] = command("hardware_bridge", kMetadataCommandInterfaces[i]);
  }
  for (std::size_t i = 0; i < kRlMetadataCommandInterfaces.size(); ++i) {
    rl_metadata_cmd_[i] = command("hardware_bridge", kRlMetadataCommandInterfaces[i]);
  }
  for (std::size_t i = 0; i < kObservationSize; ++i) {
    observation_cmd_[i] = command("hardware_bridge", "obs_current" + std::to_string(i));
  }
  const auto populate_joint_metadata = [this](
    const std::string & prefix,
    std::array<hardware_interface::LoanedCommandInterface *, kJointCount> & interfaces) {
      for (std::size_t i = 0; i < interfaces.size(); ++i) {
        interfaces[i] = command("hardware_bridge", prefix + std::to_string(i));
      }
    };
  populate_joint_metadata("action_policy", action_policy_cmd_);
  populate_joint_metadata("action_native", action_native_cmd_);
  populate_joint_metadata("action_scaled", action_scaled_cmd_);
  populate_joint_metadata("stand_target", stand_target_cmd_);
  populate_joint_metadata("rl_target", rl_target_cmd_);
  populate_joint_metadata("limited_target", limited_target_cmd_);
  populate_joint_metadata("blended_target", blended_target_cmd_);
  populate_joint_metadata("clipping_mask", clipping_mask_cmd_);
  populate_joint_metadata("joy_axis", joy_axis_cmd_);
  for (std::size_t i = 0; i < kImuInterfaces.size(); ++i) imu_state_[i] = state("trunk_imu", kImuInterfaces[i]);
  for (std::size_t i = 0; i < kHardwareInterfaces.size(); ++i) hardware_state_[i] = state("hardware_bridge", kHardwareInterfaces[i]);
  for (std::size_t i = 0; i < kLastCommandQInterfaces.size(); ++i) {
    last_command_q_state_[i] = state("hardware_bridge", kLastCommandQInterfaces[i]);
  }
  const auto missing = [](const auto * pointer) {return pointer == nullptr;};
  if (enable_cmd_ == nullptr || std::any_of(metadata_cmd_.begin(), metadata_cmd_.end(), missing) ||
    std::any_of(rl_metadata_cmd_.begin(), rl_metadata_cmd_.end(), missing) ||
    std::any_of(observation_cmd_.begin(), observation_cmd_.end(), missing) ||
    std::any_of(action_policy_cmd_.begin(), action_policy_cmd_.end(), missing) ||
    std::any_of(action_native_cmd_.begin(), action_native_cmd_.end(), missing) ||
    std::any_of(action_scaled_cmd_.begin(), action_scaled_cmd_.end(), missing) ||
    std::any_of(stand_target_cmd_.begin(), stand_target_cmd_.end(), missing) ||
    std::any_of(rl_target_cmd_.begin(), rl_target_cmd_.end(), missing) ||
    std::any_of(limited_target_cmd_.begin(), limited_target_cmd_.end(), missing) ||
    std::any_of(blended_target_cmd_.begin(), blended_target_cmd_.end(), missing) ||
    std::any_of(clipping_mask_cmd_.begin(), clipping_mask_cmd_.end(), missing) ||
    std::any_of(joy_axis_cmd_.begin(), joy_axis_cmd_.end(), missing) ||
    std::any_of(q_cmd_.begin(), q_cmd_.end(), missing) ||
    std::any_of(v_cmd_.begin(), v_cmd_.end(), missing) || std::any_of(effort_cmd_.begin(), effort_cmd_.end(), missing) ||
    std::any_of(kp_cmd_.begin(), kp_cmd_.end(), missing) || std::any_of(kd_cmd_.begin(), kd_cmd_.end(), missing) ||
    std::any_of(q_state_.begin(), q_state_.end(), missing) || std::any_of(v_state_.begin(), v_state_.end(), missing) ||
    std::any_of(effort_state_.begin(), effort_state_.end(), missing) || std::any_of(imu_state_.begin(), imu_state_.end(), missing) ||
    std::any_of(hardware_state_.begin(), hardware_state_.end(), missing) ||
    std::any_of(last_command_q_state_.begin(), last_command_q_state_.end(), missing)) {
    RCLCPP_ERROR(get_node()->get_logger(), "Required Stage 1 command/state interface is missing");
    return controller_interface::CallbackReturn::ERROR;
  }
  if (!set_command(enable_cmd_, 0.0)) return controller_interface::CallbackReturn::ERROR;
  for (auto * interface : metadata_cmd_) {
    if (!set_command(interface, 0.0)) return controller_interface::CallbackReturn::ERROR;
  }
  for (auto * interface : rl_metadata_cmd_) {
    if (!set_command(interface, 0.0)) return controller_interface::CallbackReturn::ERROR;
  }
  for (auto * interface : observation_cmd_) {
    if (!set_command(interface, 0.0)) return controller_interface::CallbackReturn::ERROR;
  }
  core_->activate();
  controller_sequence_ = 0;
  max_observed_period_seconds_ = 0.0;
  deadline_miss_count_ = 0;
  last_verified_write_sequence_ = 0;
  last_prepared_q_.fill(0.0);
  last_prepared_valid_ = false;
  composite_confirmation_reported_ = false;
  logger_flush_reported_ = false;
  logger_flush_request_sequence_ = 0;
  last_action_policy_.fill(0.0F);
  last_estimator_scaled_.fill(0.0F);
  previous_action_policy_.fill(0.0F);
  last_action_native_.fill(0.0F);
  rl_entry_initialized_ = false;
  last_inference_valid_ = false;
  last_observation_valid_ = false;
  last_target_delta_ok_ = false;
  last_inference_ms_ = 0.0;
  inference_updated_this_cycle_ = false;
  estimator_vx_integral_m_ = 0.0;
  wheel_no_slip_integral_m_ = 0.0;
  policy_elapsed_ = 0.0;
  repeated_clipping_ = 0;
  safe_hold_button_latch_.reset();
  joy_command_slew_.reset();
  last_joy_axes_.fill(0.0F);
  last_joy_command_.fill(0.0);
  last_joy_age_ms_ = 1.0e9;
  last_state_ = Stage1State::WAIT_FOR_HARDWARE;
  return controller_interface::CallbackReturn::SUCCESS;
}

void Stage1Controller::update_rl_input(Stage1Input & input, const double period_seconds)
{
  if (!stage2_enabled_) return;
  inference_updated_this_cycle_ = false;
  const JoySample * joy = joy_buffer_.readFromRT();
  std::array<float, 3> command{};
  bool joy_valid = joy != nullptr && joy->valid && joy->buttons_safe;
  if (joy_valid) {
    const int64_t now_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(
      std::chrono::steady_clock::now().time_since_epoch()).count();
    const double age = static_cast<double>(now_ns - joy->received_steady_ns) * 1.0e-9;
    last_joy_age_ms_ = age * 1000.0;
    last_joy_axes_ = joy->axes;
    joy_valid = age >= 0.0 && age <= joy_timeout_seconds_;
    const double safe_hold_value = joy->axes[static_cast<std::size_t>(joy_safe_hold_axis_)];
    if (safe_hold_button_latch_.update(
        safe_hold_value, joy_safe_hold_pressed_max_, joy_safe_hold_released_min_))
    {
      safe_hold_requested_.store(true, std::memory_order_release);
    }
    // A held stop switch is never a valid policy-command sample, including at startup.
    joy_valid = joy_valid && !safe_hold_button_latch_.pressed();
    const int ratio_index = std::clamp(
      static_cast<int>(1.0F - joy->axes[joy_speed_axis_]), 0, 2);
    const double ratio = joy_speed_ratios_[static_cast<std::size_t>(ratio_index)];
    for (std::size_t index = 0; index < command.size(); ++index) {
      const int axis = joy_command_axes_[index];
      if (axis < 0 || axis >= static_cast<int>(joy->axes.size())) {
        joy_valid = false;
        break;
      }
      command[index] = static_cast<float>(
        joy->axes[static_cast<std::size_t>(axis)] * joy_command_signs_[index] *
        joy_command_scales_[index] * ratio);
    }
    if (joy_lateral_enable_axis_ >= 0 &&
      joy_lateral_enable_axis_ < static_cast<int>(joy->axes.size()) &&
      joy->axes[static_cast<std::size_t>(joy_lateral_enable_axis_)] != 0.0F)
    {
      command[1] = 0.0F;
    }
    for (std::size_t index = 0; index < command.size(); ++index) {
      const float limit = static_cast<float>(joy_command_limits_[index]);
      command[index] = bounded_joy_command(
        command[index], limit, static_cast<float>(joy_command_gain_));
    }
  }
  command = joy_command_slew_.update(
    command, period_seconds, joy_command_ramp_rate_, joy_command_stop_seconds_);
  input.joystick_fresh = joy_valid;
  input.joystick_zero = joy_valid && std::all_of(
    command.begin(), command.end(), [this](const float value) {
      return std::abs(value) <= joy_zero_tolerance_;
    });
  for (std::size_t index = 0; index < command.size(); ++index) {
    last_joy_command_[index] = command[index];
  }

  policy_elapsed_ += period_seconds;
  // Run inference during the five-second standing window so the next control cycle
  // can select the native policy directly, without a prepare or blend state.
  const bool policy_inference_state = policy_inference_allowed(core_->state(), stage2_enabled_);
  const bool entering_rl_entry = core_->state() == Stage1State::STANDING_SETTLE &&
    !rl_entry_initialized_;
  if (policy_inference_state && policy_elapsed_ + 1e-12 >= policy_period_seconds_) {
    policy_elapsed_ = std::fmod(policy_elapsed_, policy_period_seconds_);
    ObservationInput observation_input;
    for (std::size_t index = 0; index < kJointCount; ++index) {
      observation_input.joint_position_native[index] = static_cast<float>(input.q[index]);
      observation_input.joint_velocity_native[index] = static_cast<float>(input.dq[index]);
      observation_input.previous_action_policy_order[index] = previous_action_policy_[index];
    }
    for (std::size_t index = 0; index < 4U; ++index) {
      observation_input.quaternion_xyzw[index] =
        static_cast<float>(input.quaternion_xyzw[index]);
    }
    for (std::size_t index = 0; index < 3U; ++index) {
      observation_input.angular_velocity[index] =
        static_cast<float>(input.angular_velocity[index]);
      observation_input.command_vx_vy_yaw[index] = command[index];
    }
    const auto observation = observation_builder_.build(observation_input);
    last_observation_valid_ = observation.finite;
    last_inference_valid_ = false;
    if (observation.finite && joy_valid) {
      last_observation_ = observation.values;
      if (entering_rl_entry) {
        // My26 has no history input. The first native policy evaluation begins
        // from the same zero previous-action state used by validation simulation.
        previous_action_policy_.fill(0.0F);
        repeated_clipping_ = 0U;
        rl_entry_initialized_ = true;
      }
      std::string error;
      last_inference_valid_ = policy_runner_->infer(
        last_observation_, last_action_policy_, last_estimator_scaled_,
        last_inference_ms_, error);
      inference_updated_this_cycle_ = last_inference_valid_;
      if (last_inference_valid_) {
          last_targets_ = action_adapter_.compute_native_policy(last_action_policy_);
          FloatJointArray operational_lower{};
          FloatJointArray operational_upper{};
          for (std::size_t index = 0; index < kJointCount; ++index) {
            operational_lower[index] = static_cast<float>(controller_config_.lower_limits[index]);
            operational_upper[index] = static_cast<float>(controller_config_.upper_limits[index]);
          }
          last_targets_ = action_adapter_.apply_operational_envelope(
            last_targets_, operational_lower, operational_upper);
          last_inference_valid_ = last_targets_.finite;
          last_action_native_ = last_targets_.action_native_order;
          repeated_clipping_ = last_targets_.clipping_count > 0U ?
            repeated_clipping_ + 1U : 0U;
          last_target_delta_ok_ = true;
          for (std::size_t index : {0U, 1U, 2U, 4U, 5U, 6U}) {
            const double target = last_targets_.rl_target_native[index];
            last_target_delta_ok_ = last_target_delta_ok_ &&
              target >= controller_config_.lower_limits[index] &&
              target <= controller_config_.upper_limits[index];
          }
      }
    }
  }
  input.observation_valid = last_observation_valid_;
  input.inference_valid = last_inference_valid_;
  input.inference_deadline_ok = last_inference_valid_ &&
    last_inference_ms_ <= controller_config_.max_inference_seconds * 1000.0;
  input.rl_target_delta_ok = last_target_delta_ok_;
  input.repeated_clipping = repeated_clipping_;
  for (std::size_t index = 0; index < kJointCount; ++index) {
    input.rl_mixed_target[index] = last_targets_.limited_target_native[index];
  }
}

controller_interface::return_type Stage1Controller::update(
  const rclcpp::Time &, const rclcpp::Duration & period)
{
  Stage1Input input;
  for (std::size_t i = 0; i < kJointCount; ++i) {
    input.q[i] = q_state_[i]->get_value(); input.dq[i] = v_state_[i]->get_value();
    input.effort[i] = effort_state_[i]->get_value();
  }
  input.quaternion_xyzw = {imu_state_[0]->get_value(), imu_state_[1]->get_value(), imu_state_[2]->get_value(), imu_state_[3]->get_value()};
  input.angular_velocity = {imu_state_[4]->get_value(), imu_state_[5]->get_value(), imu_state_[6]->get_value()};
  input.linear_acceleration = {imu_state_[7]->get_value(), imu_state_[8]->get_value(), imu_state_[9]->get_value()};
  input.hardware_read_valid = hardware_state_[0]->get_value() > 0.5;
  input.previous_write_success = hardware_state_[1]->get_value() > 0.5;
  input.write_sequence = static_cast<uint64_t>(hardware_state_[2]->get_value());
  input.consecutive_write_failures = static_cast<unsigned int>(hardware_state_[3]->get_value());
  input.motors_online = hardware_state_[4]->get_value() > 0.5;
  input.dropped_log_records = hardware_state_[5]->get_value();
  input.hardware_output_enabled = hardware_state_[6]->get_value() > 0.5;
  input.motor_api_write_count = static_cast<uint64_t>(hardware_state_[7]->get_value());
  input.imu_fresh = hardware_state_[8]->get_value() > 0.5;
  input.motors_fresh = hardware_state_[9]->get_value() > 0.5;
  input.joint_vectors_valid = hardware_state_[10]->get_value() > 0.5;
  input.state_values_finite = hardware_state_[11]->get_value() > 0.5;
  input.motor_status_all_online = hardware_state_[12]->get_value() > 0.5;
  input.motor_status_available = hardware_state_[13]->get_value() > 0.5;
  if (last_prepared_valid_ && input.write_sequence > last_verified_write_sequence_) {
    input.unexpected_command_clamp = false;
    for (std::size_t i = 0; i < kJointCount; ++i) {
      const double actual = last_command_q_state_[i]->get_value();
      if (!std::isfinite(actual) ||
        std::abs(actual - last_prepared_q_[i]) > command_transport_tolerance_rad_)
      {
        input.unexpected_command_clamp = true;
      }
    }
    last_verified_write_sequence_ = input.write_sequence;
  }
  input.period_seconds = period.seconds();
  if (std::isfinite(input.period_seconds)) {
    max_observed_period_seconds_ = std::max(max_observed_period_seconds_, input.period_seconds);
  }
  update_rl_input(input, input.period_seconds);
  if (safe_hold_requested_.exchange(false, std::memory_order_acq_rel)) {
    core_->request_safe_hold("OPERATOR_SAFE_HOLD");
  }
  const auto output = core_->update(input);
  if (output.state == Stage1State::RL_RUNNING && last_state_ != Stage1State::RL_RUNNING) {
    estimator_vx_integral_m_ = 0.0;
    wheel_no_slip_integral_m_ = 0.0;
  }
  if (output.state == Stage1State::RL_RUNNING && std::isfinite(input.period_seconds)) {
    estimator_vx_integral_m_ +=
      static_cast<double>(last_estimator_scaled_[0]) / kEstimatorTargetScale * input.period_seconds;
    const double wheel_common_rad_s = 0.5 * (input.dq[3] + input.dq[7]);
    wheel_no_slip_integral_m_ += wheel_common_rad_s * kWheelRadiusM * input.period_seconds;
  }
  if (output.state == Stage1State::RL_RUNNING) {
    previous_action_policy_ = last_action_policy_;
  } else if (output.state == Stage1State::STANDING_SETTLE ||
    output.state == Stage1State::SAFE_HOLD || output.state == Stage1State::FAULT)
  {
    previous_action_policy_.fill(0.0F);
  }
  if (input.period_seconds > controller_config_.max_period_seconds) {
    ++deadline_miss_count_;
    RCLCPP_ERROR_THROTTLE(
      get_node()->get_logger(), *get_node()->get_clock(), 1000,
      "CONTROL_DEADLINE_MISS: period_ms=%.3f limit_ms=%.3f max_observed_ms=%.3f "
      "count=%lu state=%s write_seq=%lu motor_writes=%lu inference_ms=%.3f",
      input.period_seconds * 1000.0, controller_config_.max_period_seconds * 1000.0,
      max_observed_period_seconds_ * 1000.0,
      static_cast<unsigned long>(deadline_miss_count_), to_string(output.state),
      static_cast<unsigned long>(input.write_sequence),
      static_cast<unsigned long>(input.motor_api_write_count), last_inference_ms_);
  }
  if (output.state == Stage1State::WAIT_FOR_HARDWARE) {
    RCLCPP_WARN_THROTTLE(
      get_node()->get_logger(), *get_node()->get_clock(), 1000,
      "WAIT_FOR_HARDWARE command-free: elapsed=%.3f stable=%.3f read_valid=%d "
      "motors_online=%d imu_fresh=%d motors_fresh=%d vectors_valid=%d finite=%d "
      "status_available=%d status_online=%d output_gate=%d",
      output.hardware_wait_elapsed, output.hardware_stable_elapsed,
      input.hardware_read_valid, input.motors_online, input.imu_fresh, input.motors_fresh,
      input.joint_vectors_valid, input.state_values_finite, input.motor_status_available,
      input.motor_status_all_online,
      input.hardware_output_enabled);
  }
  ++controller_sequence_;
  if (inference_updated_this_cycle_ && realtime_diagnostic_publisher_ &&
    realtime_diagnostic_publisher_->trylock())
  {
    auto & data = realtime_diagnostic_publisher_->msg_.data;
    std::size_t diagnostic_index = 0U;
    data[diagnostic_index++] = static_cast<double>(
      std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count());
    data[diagnostic_index++] = static_cast<double>(controller_sequence_);
    data[diagnostic_index++] = static_cast<double>(output.state);
    data[diagnostic_index++] = last_inference_ms_;
    for (const double value : last_joy_command_) data[diagnostic_index++] = value;
    for (const float value : last_estimator_scaled_) data[diagnostic_index++] = value;
    for (const float value : last_estimator_scaled_) {
      data[diagnostic_index++] = static_cast<double>(value) / kEstimatorTargetScale;
    }
    const double wheel_common_rad_s = 0.5 * (input.dq[3] + input.dq[7]);
    data[diagnostic_index++] = wheel_common_rad_s;
    data[diagnostic_index++] = wheel_common_rad_s * kWheelRadiusM;
    data[diagnostic_index++] = estimator_vx_integral_m_;
    data[diagnostic_index++] = wheel_no_slip_integral_m_;
    for (const float value : last_observation_) data[diagnostic_index++] = value;
    for (const float value : last_action_policy_) data[diagnostic_index++] = value;
    for (const double value : input.q) data[diagnostic_index++] = value;
    for (const double value : input.dq) data[diagnostic_index++] = value;
    for (const double value : input.quaternion_xyzw) data[diagnostic_index++] = value;
    for (const double value : input.angular_velocity) data[diagnostic_index++] = value;
    if (diagnostic_index == data.size()) {
      realtime_diagnostic_publisher_->unlockAndPublish();
    } else {
      realtime_diagnostic_publisher_->unlock();
    }
  }
  bool interfaces_ok = true;
  if (output.command_prepared) {
    for (std::size_t i = 0; i < kJointCount; ++i) {
      interfaces_ok = set_command(q_cmd_[i], output.q[i]) && interfaces_ok;
      interfaces_ok = set_command(v_cmd_[i], output.v[i]) && interfaces_ok;
      interfaces_ok = set_command(effort_cmd_[i], output.effort[i]) && interfaces_ok;
      interfaces_ok = set_command(kp_cmd_[i], output.kp[i]) && interfaces_ok;
      interfaces_ok = set_command(kd_cmd_[i], output.kd[i]) && interfaces_ok;
    }
    last_prepared_q_ = output.q;
    last_prepared_valid_ = true;
  } else {
    last_prepared_valid_ = false;
  }
  interfaces_ok = set_command(metadata_cmd_[0], static_cast<double>(output.state)) && interfaces_ok;
  interfaces_ok = set_command(metadata_cmd_[1], static_cast<double>(controller_sequence_)) && interfaces_ok;
  interfaces_ok = set_command(metadata_cmd_[2], output.transform_progress) && interfaces_ok;
  interfaces_ok = set_command(metadata_cmd_[3], output.settle_elapsed) && interfaces_ok;
  interfaces_ok = set_command(
    metadata_cmd_[4], output.command_prepared ? 1.0 : 0.0) && interfaces_ok;
  if (output.state == Stage1State::SAFE_HOLD && logger_flush_request_sequence_ == 0U) {
    logger_flush_request_sequence_ = controller_sequence_;
  }
  const std::array<double, 13> rl_metadata = {
    0.0, output.policy_active_alpha, output.rl_running_elapsed,
    0.0, last_inference_ms_,
    input.joystick_fresh ? 1.0 : 0.0, input.joystick_zero ? 1.0 : 0.0,
    static_cast<double>(repeated_clipping_), static_cast<double>(logger_flush_request_sequence_),
    last_joy_age_ms_, last_joy_command_[0], last_joy_command_[1], last_joy_command_[2]};
  for (std::size_t index = 0; index < rl_metadata.size(); ++index) {
    interfaces_ok = set_command(rl_metadata_cmd_[index], rl_metadata[index]) && interfaces_ok;
  }
  for (std::size_t index = 0; index < kObservationSize; ++index) {
    interfaces_ok = set_command(observation_cmd_[index], last_observation_[index]) && interfaces_ok;
  }
  for (std::size_t index = 0; index < kJointCount; ++index) {
    interfaces_ok = set_command(action_policy_cmd_[index], last_action_policy_[index]) && interfaces_ok;
    interfaces_ok = set_command(action_native_cmd_[index], last_action_native_[index]) && interfaces_ok;
    interfaces_ok = set_command(
      action_scaled_cmd_[index], last_targets_.action_scaled_native[index]) && interfaces_ok;
    interfaces_ok = set_command(
      stand_target_cmd_[index], controller_config_.stand_jpos[index]) && interfaces_ok;
    interfaces_ok = set_command(
      rl_target_cmd_[index], last_targets_.rl_target_native[index]) && interfaces_ok;
    interfaces_ok = set_command(
      limited_target_cmd_[index], last_targets_.limited_target_native[index]) && interfaces_ok;
    const double blended = (index == 3U || index == 7U) ? output.v[index] : output.q[index];
    interfaces_ok = set_command(blended_target_cmd_[index], blended) && interfaces_ok;
    interfaces_ok = set_command(
      clipping_mask_cmd_[index], last_targets_.clipping_mask[index] ? 1.0 : 0.0) &&
      interfaces_ok;
    interfaces_ok = set_command(joy_axis_cmd_[index], last_joy_axes_[index]) && interfaces_ok;
  }
  if (!interfaces_ok) {
    (void)set_command(enable_cmd_, 0.0);
    RCLCPP_ERROR(get_node()->get_logger(), "Failed to update a Stage 1 command interface");
    return controller_interface::return_type::ERROR;
  }
  if (!set_command(enable_cmd_, output.command_enable ? 1.0 : 0.0)) {
    RCLCPP_ERROR(get_node()->get_logger(), "Failed to update command_enable");
    return controller_interface::return_type::ERROR;
  }
  if (!composite_confirmation_reported_ && input.hardware_read_valid && input.motors_online &&
    input.previous_write_success && input.write_sequence > 0U && output.command_prepared &&
    output.state == Stage1State::TRANSFORM_UP) {
    std_msgs::msg::String confirmation;
    confirmation.data =
      "DIRECT_COMPOSITE_CONFIRMED;first_state_read=true;interface_claim=true;"
      "first_command_written=true;write_sequence=" + std::to_string(input.write_sequence);
    status_pub_->publish(confirmation);
    RCLCPP_INFO(get_node()->get_logger(), "%s", confirmation.data.c_str());
    composite_confirmation_reported_ = true;
  }
  if (output.state != last_state_) {
    std_msgs::msg::String message;
    message.data = std::string(to_string(output.state)) + ";fault=" + output.fault +
      ";power_cycle_required=" + (output.power_cycle_required ? "true" : "false") +
      ";read_valid=" + (input.hardware_read_valid ? "true" : "false") +
      ";motors_online=" + (input.motors_online ? "true" : "false") +
      ";imu_fresh=" + (input.imu_fresh ? "true" : "false") +
      ";motors_fresh=" + (input.motors_fresh ? "true" : "false") +
      ";vectors_valid=" + (input.joint_vectors_valid ? "true" : "false") +
      ";finite=" + (input.state_values_finite ? "true" : "false") +
      ";status_available=" + (input.motor_status_available ? "true" : "false") +
      ";status_online=" + (input.motor_status_all_online ? "true" : "false");
    if (stage2_enabled_) {
      message.data += ";joy_fresh=" + std::string(input.joystick_fresh ? "true" : "false") +
        ";joy_zero=" + (input.joystick_zero ? "true" : "false") +
        ";history_valid=not_required" +
        ";inference_ms=" + std::to_string(last_inference_ms_) +
        ";policy_active_alpha=" + std::to_string(output.policy_active_alpha) +
        ";rl_running_elapsed=" + std::to_string(output.rl_running_elapsed);
    }
    status_pub_->publish(message);
    RCLCPP_INFO(get_node()->get_logger(), "Stage1 state: %s", message.data.c_str());
    last_state_ = output.state;
  }
  if (!logger_flush_reported_ && logger_flush_request_sequence_ > 0U &&
    hardware_state_[14]->get_value() >= static_cast<double>(logger_flush_request_sequence_))
  {
    std_msgs::msg::String flushed;
    flushed.data = "LOGGER_FLUSHED;sequence=" + std::to_string(logger_flush_request_sequence_);
    status_pub_->publish(flushed);
    logger_flush_reported_ = true;
  }
  return controller_interface::return_type::OK;
}

controller_interface::CallbackReturn Stage1Controller::on_deactivate(const rclcpp_lifecycle::State &)
{
  if (metadata_cmd_[4]) (void)set_command(metadata_cmd_[4], 0.0);
  if (enable_cmd_) (void)set_command(enable_cmd_, 0.0);
  return controller_interface::CallbackReturn::SUCCESS;
}
}  // namespace tita_stage1_controller

PLUGINLIB_EXPORT_CLASS(
  tita_stage1_controller::Stage1Controller, controller_interface::ControllerInterface)
