#ifndef TITA_STAGE1_CONTROLLER__STAGE1_CORE_HPP_
#define TITA_STAGE1_CONTROLLER__STAGE1_CORE_HPP_

#include <array>
#include <cstdint>
#include <string>

namespace tita_stage1_controller
{
constexpr std::size_t kJointCount = 8;
using JointArray = std::array<double, kJointCount>;

enum class Stage1State
{
  WAIT_FOR_HARDWARE,
  MEASURE_INITIAL_POSE,
  TRANSFORM_UP,
  STANDING_SETTLE,
  RL_HANDOFF,
  RL_PREPARE,
  RL_BLEND,
  RL_RUNNING,
  SAFE_HOLD,
  FAULT
};

struct Stage1Config
{
  JointArray fold_jpos{};
  JointArray stand_jpos{};
  JointArray transform_kp{};
  JointArray transform_kd{};
  JointArray ff_effort{};
  JointArray transition_lower_limits{};
  JointArray transition_upper_limits{};
  JointArray lower_limits{};
  JointArray upper_limits{};
  JointArray effort_limits{};
  JointArray rl_kp{};
  JointArray rl_kd{};
  double fold_timer{4.0};
  double stand_timer{2.0};
  double settle_seconds{5.0};
  double stand_error_rad{0.15};
  double wheel_velocity_rad_s{0.3};
  double max_roll_rad{0.35};
  double max_pitch_rad{0.35};
  double fall_tilt_rad{0.65};
  double max_angular_velocity_rad_s{1.5};
  double max_target_slew_rad_s{1.5};
  double max_period_seconds{0.01};
  double hardware_state_wait_timeout_seconds{1.0};
  double hardware_state_stable_seconds{0.10};
  double operational_entry_timeout_seconds{2.0};
  double operational_entry_stable_seconds{0.10};
  double operational_entry_margin_rad{0.02};
  double operational_entry_max_joint_velocity_rad_s{0.5};
  double operational_envelope_tolerance_rad{1.0e-6};
  unsigned int write_failure_threshold{3};
  bool stage2_enabled{false};
  JointArray policy_stand_jpos{};
  double handoff_seconds{3.0};
  double handoff_settle_seconds{1.0};
  double rl_prepare_seconds{1.0};
  double rl_blend_seconds{1.0};
  double rl_running_seconds{2.0};
  double max_leg_target_delta_rad{0.25};
  double max_leg_target_slew_rad_s{0.5};
  double max_wheel_velocity_rad_s{5.0};
  double max_wheel_accel_rad_s{5.0};
  double max_inference_seconds{0.010};
  unsigned int max_repeated_clipping{5};
  bool allow_clipped_rl_diagnostic{false};
  bool require_zero_joystick{true};
};

struct Stage1Input
{
  JointArray q{};
  JointArray dq{};
  JointArray effort{};
  std::array<double, 4> quaternion_xyzw{0.0, 0.0, 0.0, 1.0};
  std::array<double, 3> angular_velocity{};
  std::array<double, 3> linear_acceleration{0.0, 0.0, 9.81};
  bool hardware_read_valid{false};
  bool motors_online{false};
  bool imu_fresh{false};
  bool motors_fresh{false};
  bool joint_vectors_valid{false};
  bool state_values_finite{false};
  bool motor_status_all_online{false};
  bool motor_status_available{false};
  bool previous_write_success{false};
  bool hardware_output_enabled{false};
  uint64_t write_sequence{0};
  uint64_t motor_api_write_count{0};
  unsigned int consecutive_write_failures{0};
  bool unexpected_command_clamp{false};
  double dropped_log_records{0.0};
  double period_seconds{0.002};
  bool joystick_fresh{false};
  bool joystick_zero{false};
  bool observation_valid{false};
  bool history_complete{false};
  bool inference_valid{false};
  bool inference_deadline_ok{false};
  bool rl_target_delta_ok{false};
  unsigned int repeated_clipping{0};
  JointArray rl_mixed_target{};  // leg slots are q; wheel slots are dq.
};

struct Stage1Output
{
  JointArray q{};
  JointArray v{};
  JointArray kp{};
  JointArray kd{};
  JointArray effort{};
  Stage1State state{Stage1State::WAIT_FOR_HARDWARE};
  bool command_enable{false};
  bool command_prepared{false};
  bool power_cycle_required{false};
  double transform_progress{0.0};
  double handoff_progress{0.0};
  double settle_elapsed{0.0};
  double hardware_wait_elapsed{0.0};
  double hardware_stable_elapsed{0.0};
  double rl_prepare_elapsed{0.0};
  double rl_blend_alpha{0.0};
  double rl_running_elapsed{0.0};
  std::string fault;
};

class SafeHoldButtonLatch
{
public:
  bool update(double value, double pressed_max, double released_min);
  bool pressed() const {return pressed_;}
  void reset();

private:
  bool initialized_{false};
  bool released_seen_{false};
  bool pressed_{false};
};

float bounded_joy_command(float value, float limit, float gain);

class Stage1Core
{
public:
  explicit Stage1Core(Stage1Config config);
  bool valid_config() const;
  bool command_envelopes_valid() const;
  void activate();
  void request_safe_hold(const std::string & reason);
  Stage1Output update(const Stage1Input & input);
  Stage1State state() const {return state_;}
  const JointArray & measured_initial_pose() const {return initial_q_;}

private:
  bool finite_input(const Stage1Input & input) const;
  bool within_transition_envelope(const JointArray & q) const;
  bool within_operational_envelope(const JointArray & q) const;
  bool stable_standing(const Stage1Input & input) const;
  bool stable_operational_entry(const Stage1Input & input) const;
  Stage1Output hard_fault(const std::string & fault);
  void enter_safe_hold(const std::string & fault);
  JointArray interpolate(const JointArray & a, const JointArray & b, double alpha) const;
  JointArray smooth_interpolate(const JointArray & a, const JointArray & b, double alpha) const;
  Stage1Output make_output(const Stage1Input & input, const JointArray & target);
  Stage1Output make_rl_output(const Stage1Input & input, double alpha);
  bool rl_sample_valid(const Stage1Input & input) const;

  Stage1Config config_;
  Stage1State state_{Stage1State::WAIT_FOR_HARDWARE};
  JointArray initial_q_{};
  JointArray last_target_{};
  bool initial_captured_{false};
  double phase_elapsed_{0.0};
  double settle_elapsed_{0.0};
  double hardware_wait_elapsed_{0.0};
  double hardware_stable_elapsed_{0.0};
  double operational_entry_stable_elapsed_{0.0};
  double fold_duration_{0.0};
  double rl_prepare_elapsed_{0.0};
  double handoff_elapsed_{0.0};
  double rl_blend_elapsed_{0.0};
  double rl_running_elapsed_{0.0};
  JointArray last_velocity_target_{};
  std::string fault_;
};

const char * to_string(Stage1State state);
bool policy_inference_allowed(Stage1State state, bool stage2_enabled);
}  // namespace tita_stage1_controller
#endif
