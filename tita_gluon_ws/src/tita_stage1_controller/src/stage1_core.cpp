#include "tita_stage1_controller/stage1_core.hpp"

#include <algorithm>
#include <cmath>
#include <utility>

namespace tita_stage1_controller
{
namespace
{
double clamp01(double value) {return std::clamp(value, 0.0, 1.0);}
bool finite(double value) {return std::isfinite(value);}
}  // namespace

Stage1Core::Stage1Core(Stage1Config config) : config_(std::move(config)) {}

bool SafeHoldButtonLatch::update(
  const double value, const double pressed_max, const double released_min)
{
  if (!std::isfinite(value) || !std::isfinite(pressed_max) ||
    !std::isfinite(released_min) || pressed_max >= released_min)
  {
    return false;
  }
  const bool pressed_now = value <= pressed_max;
  const bool released_now = value >= released_min;
  if (!initialized_) {
    initialized_ = true;
    pressed_ = pressed_now;
    released_seen_ = released_now;
    return false;
  }
  if (released_now) {
    pressed_ = false;
    released_seen_ = true;
    return false;
  }
  if (pressed_now) {
    const bool trigger = released_seen_ && !pressed_;
    pressed_ = true;
    if (trigger) released_seen_ = false;
    return trigger;
  }
  return false;
}

void SafeHoldButtonLatch::reset()
{
  initialized_ = false;
  released_seen_ = false;
  pressed_ = false;
}

float bounded_joy_command(const float value, const float limit, const float gain)
{
  if (!std::isfinite(value) || !std::isfinite(limit) || !std::isfinite(gain) ||
    limit < 0.0F || gain <= 0.0F || gain > 1.0F)
  {
    return 0.0F;
  }
  return std::clamp(value, -limit, limit) * gain;
}

std::array<float, 3> JoystickCommandSlew::update(
  const std::array<float, 3> & target, const double period_seconds,
  const double ramp_rate, const double stop_seconds)
{
  if (!std::isfinite(period_seconds) || period_seconds < 0.0 ||
    !std::isfinite(ramp_rate) || ramp_rate <= 0.0 ||
    !std::isfinite(stop_seconds) || stop_seconds <= 0.0)
  {
    reset();
    return command_;
  }
  for (std::size_t index = 0; index < command_.size(); ++index) {
    if (!std::isfinite(target[index])) {
      reset();
      return command_;
    }
    if (target[index] == 0.0F) {
      if (!stopping_[index]) {
        stopping_[index] = true;
        stop_start_[index] = command_[index];
        stop_elapsed_[index] = 0.0;
      }
      stop_elapsed_[index] = std::min(stop_elapsed_[index] + period_seconds, stop_seconds);
      const double remaining = 1.0 - stop_elapsed_[index] / stop_seconds;
      command_[index] = static_cast<float>(stop_start_[index] * remaining);
      if (stop_elapsed_[index] >= stop_seconds) command_[index] = 0.0F;
      continue;
    }
    stopping_[index] = false;
    stop_elapsed_[index] = 0.0;
    const float max_step = static_cast<float>(ramp_rate * period_seconds);
    const float delta = std::clamp(target[index] - command_[index], -max_step, max_step);
    command_[index] += delta;
  }
  return command_;
}

void JoystickCommandSlew::reset()
{
  command_.fill(0.0F);
  stop_start_.fill(0.0F);
  stop_elapsed_.fill(0.0);
  stopping_.fill(false);
}

bool Stage1Core::valid_config() const
{
  if (!(config_.fold_timer > 0.0 && config_.stand_timer > 0.0 &&
    config_.settle_seconds >= 5.0 &&
    config_.settle_timeout_seconds >= config_.settle_seconds &&
    config_.max_target_slew_rad_s > 0.0 &&
    config_.hardware_state_wait_timeout_seconds > 0.0 &&
    config_.hardware_state_stable_seconds > 0.0 &&
    config_.hardware_state_stable_seconds <= config_.hardware_state_wait_timeout_seconds &&
    config_.operational_entry_timeout_seconds > 0.0 &&
    config_.operational_entry_stable_seconds > 0.0 &&
    config_.operational_entry_margin_rad > 0.0 &&
    config_.operational_entry_max_joint_velocity_rad_s > 0.0 &&
    config_.operational_envelope_tolerance_rad >= 0.0 &&
    config_.write_failure_threshold > 0)) return false;
  if (config_.stage2_enabled && !(
      (config_.rl_running_seconds == 0.0 ||
      (config_.rl_running_seconds >= 1.0 && config_.rl_running_seconds <= 3.0)) &&
      config_.max_leg_target_delta_rad > 0.0 &&
      config_.max_leg_target_slew_rad_s > 0.0 &&
      config_.max_wheel_velocity_rad_s > 0.0 &&
      config_.max_wheel_accel_rad_s > 0.0 && config_.max_inference_seconds > 0.0)) return false;
  for (std::size_t i = 0; i < kJointCount; ++i) {
    if (!finite(config_.fold_jpos[i]) || !finite(config_.stand_jpos[i]) ||
      !finite(config_.transform_kp[i]) || !finite(config_.transform_kd[i]) ||
      !finite(config_.ff_effort[i]) ||
      !finite(config_.transition_lower_limits[i]) ||
      !finite(config_.transition_upper_limits[i]) ||
      !finite(config_.lower_limits[i]) || !finite(config_.upper_limits[i]) ||
      !finite(config_.rl_kp[i]) || !finite(config_.rl_kd[i]) ||
      config_.transition_lower_limits[i] >= config_.transition_upper_limits[i] ||
      config_.lower_limits[i] >= config_.upper_limits[i] ||
      config_.transition_lower_limits[i] > config_.lower_limits[i] ||
      config_.transition_upper_limits[i] < config_.upper_limits[i] ||
      config_.effort_limits[i] <= 0.0 ||
      config_.stand_jpos[i] < config_.lower_limits[i] ||
      config_.stand_jpos[i] > config_.upper_limits[i]) return false;
  }
  return true;
}

bool Stage1Core::command_envelopes_valid() const
{
  if (!valid_config()) return false;
  for (std::size_t i = 0; i < kJointCount; ++i) {
    if (config_.fold_jpos[i] < config_.transition_lower_limits[i] ||
      config_.fold_jpos[i] > config_.transition_upper_limits[i]) return false;
  }
  return true;
}

void Stage1Core::activate()
{
  state_ = Stage1State::WAIT_FOR_HARDWARE;
  initial_captured_ = false;
  phase_elapsed_ = 0.0;
  settle_elapsed_ = 0.0;
  settle_window_elapsed_ = 0.0;
  hardware_wait_elapsed_ = 0.0;
  hardware_stable_elapsed_ = 0.0;
  operational_entry_stable_elapsed_ = 0.0;
  fold_duration_ = 0.0;
  rl_running_elapsed_ = 0.0;
  last_velocity_target_.fill(0.0);
  fault_.clear();
}

bool Stage1Core::finite_input(const Stage1Input & input) const
{
  for (std::size_t i = 0; i < kJointCount; ++i) {
    if (!finite(input.q[i]) || !finite(input.dq[i]) || !finite(input.effort[i])) return false;
  }
  for (double value : input.quaternion_xyzw) if (!finite(value)) return false;
  for (double value : input.angular_velocity) if (!finite(value)) return false;
  for (double value : input.linear_acceleration) if (!finite(value)) return false;
  return finite(input.period_seconds) && input.period_seconds > 0.0;
}

bool Stage1Core::within_transition_envelope(const JointArray & q) const
{
  for (std::size_t i = 0; i < kJointCount; ++i) {
    if (q[i] < config_.transition_lower_limits[i] ||
      q[i] > config_.transition_upper_limits[i]) return false;
  }
  return true;
}

bool Stage1Core::within_operational_envelope(const JointArray & q) const
{
  for (std::size_t i = 0; i < kJointCount; ++i) {
    if (q[i] < config_.lower_limits[i] - config_.operational_envelope_tolerance_rad ||
      q[i] > config_.upper_limits[i] + config_.operational_envelope_tolerance_rad) return false;
  }
  return true;
}

bool Stage1Core::stable_standing(const Stage1Input & input) const
{
  if (!within_operational_envelope(input.q)) return false;
  for (std::size_t i : {0U, 1U, 2U, 4U, 5U, 6U}) {
    if (std::abs(input.q[i] - config_.stand_jpos[i]) > config_.stand_error_rad) return false;
  }
  if (std::abs(input.dq[3]) > config_.wheel_velocity_rad_s ||
    std::abs(input.dq[7]) > config_.wheel_velocity_rad_s) return false;
  const auto & q = input.quaternion_xyzw;
  const double roll = std::atan2(2.0 * (q[3] * q[0] + q[1] * q[2]),
    1.0 - 2.0 * (q[0] * q[0] + q[1] * q[1]));
  const double pitch = std::asin(std::clamp(2.0 * (q[3] * q[1] - q[2] * q[0]), -1.0, 1.0));
  if (std::abs(roll) > config_.max_roll_rad || std::abs(pitch) > config_.max_pitch_rad) return false;
  const double omega = std::sqrt(
    input.angular_velocity[0] * input.angular_velocity[0] +
    input.angular_velocity[1] * input.angular_velocity[1] +
    input.angular_velocity[2] * input.angular_velocity[2]);
  if (omega > config_.max_angular_velocity_rad_s) return false;
  const double accel_norm = std::sqrt(
    input.linear_acceleration[0] * input.linear_acceleration[0] +
    input.linear_acceleration[1] * input.linear_acceleration[1] +
    input.linear_acceleration[2] * input.linear_acceleration[2]);
  return accel_norm > 5.0 && accel_norm < 15.0 && input.dropped_log_records == 0.0;
}

bool Stage1Core::stable_operational_entry(const Stage1Input & input) const
{
  if (!stable_standing(input)) return false;
  for (std::size_t index : {0U, 1U, 2U, 4U, 5U, 6U}) {
    if (input.q[index] < config_.lower_limits[index] + config_.operational_entry_margin_rad ||
      input.q[index] > config_.upper_limits[index] - config_.operational_entry_margin_rad ||
      std::abs(input.dq[index]) > config_.operational_entry_max_joint_velocity_rad_s)
    {
      return false;
    }
  }
  return true;
}

void Stage1Core::enter_safe_hold(const std::string & fault)
{
  fault_ = fault;
  state_ = initial_captured_ ? Stage1State::SAFE_HOLD : Stage1State::FAULT;
}

void Stage1Core::request_safe_hold(const std::string & reason)
{
  enter_safe_hold(reason.empty() ? "OPERATOR_SAFE_HOLD" : reason);
}

Stage1Output Stage1Core::hard_fault(const std::string & fault)
{
  fault_ = fault;
  state_ = Stage1State::FAULT;
  Stage1Output output;
  output.state = state_;
  output.fault = fault_;
  return output;
}

JointArray Stage1Core::interpolate(
  const JointArray & a, const JointArray & b, const double alpha) const
{
  JointArray result{};
  for (std::size_t i = 0; i < kJointCount; ++i) result[i] = a[i] + clamp01(alpha) * (b[i] - a[i]);
  return result;
}

Stage1Output Stage1Core::make_output(const Stage1Input & input, const JointArray & requested)
{
  Stage1Output output;
  output.state = state_;
  output.command_enable = initial_captured_ && state_ != Stage1State::FAULT;
  output.command_prepared = output.command_enable;
  output.power_cycle_required = state_ == Stage1State::SAFE_HOLD;
  output.transform_progress = phase_elapsed_ /
    std::max(1e-9, fold_duration_ + config_.stand_timer);
  output.transform_progress = clamp01(output.transform_progress);
  output.settle_elapsed = settle_elapsed_;
  output.hardware_wait_elapsed = hardware_wait_elapsed_;
  output.hardware_stable_elapsed = hardware_stable_elapsed_;
  output.policy_active_alpha = state_ == Stage1State::RL_RUNNING ? 1.0 : 0.0;
  output.rl_running_elapsed = rl_running_elapsed_;
  output.fault = fault_;
  const bool rl_command_state = state_ == Stage1State::RL_RUNNING;
  const double max_delta =
    (rl_command_state ? config_.max_leg_target_slew_rad_s : config_.max_target_slew_rad_s) *
    input.period_seconds;
  for (std::size_t i = 0; i < kJointCount; ++i) {
    output.q[i] = state_ == Stage1State::RL_RUNNING ? requested[i] :
      std::clamp(requested[i], last_target_[i] - max_delta, last_target_[i] + max_delta);
    output.v[i] = 0.0;
    output.kp[i] = config_.transform_kp[i];
    output.kd[i] = config_.transform_kd[i];
    output.effort[i] = std::clamp(config_.ff_effort[i],
      -config_.effort_limits[i], config_.effort_limits[i]);
  }
  for (std::size_t wheel : {3U, 7U}) {
    output.q[wheel] = 0.0;
    output.v[wheel] = 0.0;
    output.kp[wheel] = 0.0;
    output.effort[wheel] = 0.0;
  }
  if (state_ == Stage1State::SAFE_HOLD) {
    output.effort.fill(0.0);
    const double max_wheel_delta = config_.max_wheel_accel_rad_s * input.period_seconds;
    for (std::size_t wheel : {3U, 7U}) {
      output.v[wheel] = std::clamp(
        0.0, last_velocity_target_[wheel] - max_wheel_delta,
        last_velocity_target_[wheel] + max_wheel_delta);
      last_velocity_target_[wheel] = output.v[wheel];
    }
  }
  // SAFE_HOLD can be entered while TransformUp is still legitimately using the
  // wider transition envelope.  Keep that envelope only while the previously
  // written target has not yet slewed back into the operational envelope;
  // otherwise a deadline/watchdog event can turn a safe transition into a
  // spurious hard fault on the same cycle.
  const bool transition_state =
    state_ == Stage1State::MEASURE_INITIAL_POSE || state_ == Stage1State::TRANSFORM_UP ||
    (state_ == Stage1State::SAFE_HOLD && !within_operational_envelope(last_target_));
  const bool envelope_valid = transition_state ?
    within_transition_envelope(output.q) : within_operational_envelope(output.q);
  if (!envelope_valid) return hard_fault(
      transition_state ? "TRANSITION_COMMAND_ENVELOPE_EXCEEDED" :
      "OPERATIONAL_COMMAND_ENVELOPE_EXCEEDED");
  last_target_ = output.q;
  return output;
}

bool Stage1Core::rl_sample_valid(const Stage1Input & input) const
{
  const bool policy_envelope_valid = config_.allow_clipped_rl_diagnostic ||
    (input.rl_target_delta_ok &&
    input.repeated_clipping <= config_.max_repeated_clipping);
  if (!(input.joystick_fresh &&
    (!config_.require_zero_joystick || input.joystick_zero) && input.observation_valid &&
    input.inference_valid && input.inference_deadline_ok &&
    policy_envelope_valid))
  {
    return false;
  }
  for (std::size_t index = 0; index < kJointCount; ++index) {
    if (!finite(input.rl_mixed_target[index])) return false;
    if (index != 3U && index != 7U && (
      input.rl_mixed_target[index] <
      config_.lower_limits[index] - config_.operational_envelope_tolerance_rad ||
      input.rl_mixed_target[index] >
      config_.upper_limits[index] + config_.operational_envelope_tolerance_rad))
    {
      return false;
    }
  }
  return true;
}

Stage1Output Stage1Core::make_rl_output(const Stage1Input & input)
{
  JointArray requested = input.rl_mixed_target;
  for (std::size_t index : {0U, 1U, 2U, 4U, 5U, 6U}) {
    requested[index] = input.rl_mixed_target[index];
  }
  auto output = make_output(input, requested);
  if (output.state == Stage1State::FAULT) return output;
  output.policy_active_alpha = 1.0;
  output.rl_running_elapsed = rl_running_elapsed_;
  for (std::size_t wheel : {3U, 7U}) {
    output.v[wheel] = input.rl_mixed_target[wheel];
    last_velocity_target_[wheel] = output.v[wheel];
  }
  for (std::size_t index = 0; index < kJointCount; ++index) {
    output.kp[index] = config_.rl_kp[index];
    output.kd[index] = config_.rl_kd[index];
    output.effort[index] = 0.0;
  }
  return output;
}

Stage1Output Stage1Core::update(const Stage1Input & input)
{
  if (!valid_config()) {
    fault_ = "INVALID_CONFIG";
    state_ = Stage1State::FAULT;
    Stage1Output output;
    output.state = state_;
    output.fault = fault_;
    return output;
  }
  if (!command_envelopes_valid()) return hard_fault("INVALID_COMMAND_ENVELOPES");
  if (input.unexpected_command_clamp) return hard_fault("UNEXPECTED_COMMAND_CLAMP");
  const bool state_valid = input.hardware_read_valid && input.motors_online &&
    input.hardware_output_enabled &&
    finite_input(input);
  if (state_ == Stage1State::WAIT_FOR_HARDWARE) {
    hardware_wait_elapsed_ += input.period_seconds;
    if (!state_valid || input.period_seconds > config_.max_period_seconds) {
      hardware_stable_elapsed_ = 0.0;
      if (hardware_wait_elapsed_ + 1e-9 >= config_.hardware_state_wait_timeout_seconds) {
        return hard_fault("HARDWARE_STATE_WAIT_TIMEOUT");
      }
      Stage1Output output;
      output.state = state_;
      output.hardware_wait_elapsed = hardware_wait_elapsed_;
      output.hardware_stable_elapsed = hardware_stable_elapsed_;
      return output;
    }
    hardware_stable_elapsed_ += input.period_seconds;
    if (hardware_stable_elapsed_ + 1e-9 < config_.hardware_state_stable_seconds) {
      Stage1Output output;
      output.state = state_;
      output.hardware_wait_elapsed = hardware_wait_elapsed_;
      output.hardware_stable_elapsed = hardware_stable_elapsed_;
      return output;
    }
  }
  if (!state_valid) {
    enter_safe_hold("STALE_OR_INVALID_HARDWARE_STATE");
    const JointArray target = initial_captured_ ? config_.stand_jpos : JointArray{};
    if (initial_captured_) return make_output(input, target);
    Stage1Output output;
    output.state = state_;
    output.fault = fault_;
    return output;
  }
  if (!within_transition_envelope(input.q)) {
    return hard_fault(
      initial_captured_ ? "TRANSITION_ENVELOPE_EXCEEDED" :
      "INITIAL_POSE_OUTSIDE_TRANSITION_ENVELOPE");
  }
  const auto & orientation = input.quaternion_xyzw;
  const double roll = std::atan2(
    2.0 * (orientation[3] * orientation[0] + orientation[1] * orientation[2]),
    1.0 - 2.0 * (orientation[0] * orientation[0] + orientation[1] * orientation[1]));
  const double pitch = std::asin(std::clamp(
    2.0 * (orientation[3] * orientation[1] - orientation[2] * orientation[0]), -1.0, 1.0));
  if (std::abs(roll) > config_.fall_tilt_rad || std::abs(pitch) > config_.fall_tilt_rad) {
    enter_safe_hold("FALL_TILT");
    if (!initial_captured_) {
      Stage1Output output;
      output.state = state_;
      output.fault = fault_;
      return output;
    }
  }
  const double angular_velocity_norm = std::sqrt(
    input.angular_velocity[0] * input.angular_velocity[0] +
    input.angular_velocity[1] * input.angular_velocity[1] +
    input.angular_velocity[2] * input.angular_velocity[2]);
  if (state_ == Stage1State::RL_RUNNING &&
    angular_velocity_norm > config_.max_angular_velocity_rad_s)
  {
    enter_safe_hold("EXCESSIVE_ANGULAR_VELOCITY");
  }
  if (input.period_seconds > config_.max_period_seconds) {
    enter_safe_hold("CONTROL_DEADLINE_MISS");
  }
  if (input.consecutive_write_failures >= config_.write_failure_threshold) {
    enter_safe_hold("HARDWARE_WRITE_FAILURE");
  }
  if (state_ == Stage1State::WAIT_FOR_HARDWARE) {
    initial_q_ = input.q;
    last_target_ = input.q;
    initial_captured_ = true;
    double max_fold_delta = 0.0;
    for (std::size_t i = 0; i < kJointCount; ++i) {
      max_fold_delta = std::max(max_fold_delta, std::abs(initial_q_[i] - config_.fold_jpos[i]));
    }
    fold_duration_ = std::max(input.period_seconds, config_.fold_timer * max_fold_delta);
    state_ = Stage1State::MEASURE_INITIAL_POSE;
    JointArray target = initial_q_;
    target[3] = target[7] = 0.0;
    return make_output(input, target);
  }
  if (state_ == Stage1State::MEASURE_INITIAL_POSE) {
    state_ = Stage1State::TRANSFORM_UP;
    phase_elapsed_ = 0.0;
  }
  if (state_ == Stage1State::TRANSFORM_UP) {
    phase_elapsed_ += input.period_seconds;
    JointArray target{};
    if (phase_elapsed_ <= fold_duration_) {
      target = interpolate(initial_q_, config_.fold_jpos, phase_elapsed_ / fold_duration_);
    } else {
      target = interpolate(config_.fold_jpos, config_.stand_jpos,
        (phase_elapsed_ - fold_duration_) / config_.stand_timer);
    }
    const double transform_end = fold_duration_ + config_.stand_timer;
    if (phase_elapsed_ >= transform_end) {
      target = config_.stand_jpos;
      if (stable_operational_entry(input)) {
        operational_entry_stable_elapsed_ += input.period_seconds;
      } else {
        operational_entry_stable_elapsed_ = 0.0;
      }
      if (operational_entry_stable_elapsed_ + 1e-9 >=
        config_.operational_entry_stable_seconds)
      {
        state_ = Stage1State::STANDING_SETTLE;
        settle_elapsed_ = 0.0;
        settle_window_elapsed_ = 0.0;
      } else if (
        phase_elapsed_ >= transform_end + config_.operational_entry_timeout_seconds)
      {
        enter_safe_hold("OPERATIONAL_ENVELOPE_ENTRY_TIMEOUT");
      }
    }
    return make_output(input, target);
  }
  if (state_ == Stage1State::STANDING_SETTLE) {
    settle_window_elapsed_ += input.period_seconds;
    if (!within_operational_envelope(input.q)) {
      settle_elapsed_ = 0.0;
      enter_safe_hold("OPERATIONAL_ENVELOPE_EXCEEDED");
      return make_output(input, config_.stand_jpos);
    }
    if (stable_standing(input)) settle_elapsed_ += input.period_seconds;
    else settle_elapsed_ = 0.0;
    if (settle_elapsed_ + 1e-9 >= config_.settle_seconds) {
      if (!config_.stage2_enabled) {
        state_ = Stage1State::SAFE_HOLD;
        fault_.clear();
        return make_output(input, config_.stand_jpos);
      }
      if (!rl_sample_valid(input)) {
        enter_safe_hold("RL_ENTRY_WATCHDOG");
        return make_output(input, config_.stand_jpos);
      }
      state_ = Stage1State::RL_RUNNING;
      rl_running_elapsed_ = 0.0;
      fault_.clear();
      return make_rl_output(input);
    } else if (settle_window_elapsed_ + 1e-9 >= config_.settle_timeout_seconds) {
      enter_safe_hold("STANDING_SETTLE_TIMEOUT");
    }
    return make_output(input, config_.stand_jpos);
  }
  if (state_ == Stage1State::RL_RUNNING) {
    if (!within_operational_envelope(input.q)) {
      enter_safe_hold("RL_OPERATIONAL_ENVELOPE_EXCEEDED");
      return make_output(input, config_.stand_jpos);
    }
    if (!rl_sample_valid(input)) {
      enter_safe_hold("RL_RUNNING_WATCHDOG");
      return make_output(input, config_.stand_jpos);
    }
    rl_running_elapsed_ += input.period_seconds;
    if (config_.rl_running_seconds > 0.0 &&
      rl_running_elapsed_ + 1e-9 >= config_.rl_running_seconds)
    {
      state_ = Stage1State::SAFE_HOLD;
      fault_.clear();
      return make_output(input, config_.stand_jpos);
    }
    return make_rl_output(input);
  }
  if (state_ == Stage1State::SAFE_HOLD) return make_output(input, config_.stand_jpos);
  Stage1Output output;
  output.state = state_;
  output.fault = fault_;
  return output;
}

const char * to_string(const Stage1State state)
{
  switch (state) {
    case Stage1State::WAIT_FOR_HARDWARE: return "WAIT_FOR_HARDWARE";
    case Stage1State::MEASURE_INITIAL_POSE: return "MEASURE_INITIAL_POSE";
    case Stage1State::TRANSFORM_UP: return "TRANSFORM_UP";
    case Stage1State::STANDING_SETTLE: return "STANDING_SETTLE";
    case Stage1State::RL_RUNNING: return "RL_RUNNING";
    case Stage1State::SAFE_HOLD: return "SAFE_HOLD";
    case Stage1State::FAULT: return "FAULT";
  }
  return "FAULT";
}

bool policy_inference_allowed(const Stage1State state, const bool stage2_enabled)
{
  return stage2_enabled &&
    (state == Stage1State::STANDING_SETTLE || state == Stage1State::RL_RUNNING);
}
}  // namespace tita_stage1_controller
