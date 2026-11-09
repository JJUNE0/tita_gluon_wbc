// Observation layout and native joint PD. C++ port of sim2sim adapter.py.
// The launch file flattens the checkpoint config.json into one entry per observation element
// and per action, so this file only loops.
#pragma once

#include <algorithm>
#include <array>
#include <cmath>
#include <limits>
#include <stdexcept>
#include <vector>

#include "tita_controller/state_machine.hpp"
#include "tita_controller/pose_command.hpp"

namespace tita
{
// Observation element sources (must match OBS_KINDS in launch/tita.launch.py).
enum ObsKind { AngVel, Gravity, Command, JointPos, JointVel, LastAction, Zero, WheelPositionError, HeadingError, SupportMode, PoseCommands };

struct ObsElement { int kind; int index; double scale, low, high; };
struct ActionTerm { int joint; bool velocity; double scale, offset, low, high; };

struct WheelPositionConfig
{
  double radius{0.}, clip_m{0.};
  std::array<double, 3> zero_thresholds{};
  std::array<double, 2> velocity_thresholds{};
  bool velocity_gated{false}, moving_anchor{false};
};

// Gyro heading error (training GyroHeadingError / sim2sim adapter.py heading_error): inside the command zero band and
// after warmup, integrate (gyro z - bias) * dt; 0 otherwise; output clipped, internal integral kept.
struct HeadingConfig
{
  double clip_rad{0.}, warmup_s{0.}, dt{0.};
  std::array<double, 3> zero_thresholds{};
};

struct RobotState
{
  Joints joint_pos{}, joint_vel{};
  std::array<double, 4> quat_wxyz{1., 0., 0., 0.};
  std::array<double, 3> ang_vel{};
  // Set by encoder/IMU contact kinematics before building velocity-gated observations.
  std::array<double, 3> lin_vel_b{
    std::numeric_limits<double>::quiet_NaN(), std::numeric_limits<double>::quiet_NaN(),
    std::numeric_limits<double>::quiet_NaN()};
  int support_mode{2};
  std::array<double, 3> pose_command{0., 0., .335};  // roll rad, pitch rad, absolute height m
};

// R(q)^T [0, 0, -1]
inline std::array<double, 3> projected_gravity(const std::array<double, 4> & q)
{
  const double w = q[0], x = q[1], y = q[2], z = q[3];
  return {-2. * (x * z - w * y), -2. * (y * z + w * x), -(1. - 2. * (x * x + y * y))};
}

inline bool exceeds_fall_tilt(const std::array<double, 4> & quaternion, double limit_rad)
{
  const auto gravity = projected_gravity(quaternion);
  return std::acos(std::clamp(-gravity[2], -1., 1.)) > limit_rad;
}

class ObservationBuilder
{
public:
  ObservationBuilder(std::vector<ObsElement> layout, Joints default_pos, Joints default_vel,
    WheelPositionConfig position = {}, HeadingConfig heading = {}, PoseCommandConfig pose = {})
  : layout_(std::move(layout)), default_pos_(default_pos), default_vel_(default_vel), position_(position),
    heading_cfg_(heading), pose_cfg_(pose)
  {
    heading_enabled_ = std::any_of(layout_.begin(), layout_.end(),
      [](const auto & e) {return e.kind == HeadingError;});
    if (heading_enabled_) {
      if (!std::isfinite(heading.clip_rad) || heading.clip_rad <= 0. || !std::isfinite(heading.warmup_s) ||
        heading.warmup_s < 0. || !std::isfinite(heading.dt) || heading.dt <= 0. ||
        !std::all_of(heading.zero_thresholds.begin(), heading.zero_thresholds.end(),
          [](double x) {return std::isfinite(x) && x >= 0.;}))
      {
        throw std::runtime_error("invalid heading error parameters");
      }
      heading_warmup_steps_ = std::max<long>(1, std::lround(heading.warmup_s / heading.dt));
    }
    position_enabled_ = std::any_of(layout_.begin(), layout_.end(),
      [](const auto & e) {return e.kind == WheelPositionError;});
    if (position_enabled_ && (!std::isfinite(position.radius) || position.radius <= 0. ||
      !std::isfinite(position.clip_m) || position.clip_m <= 0. ||
      !std::all_of(position.zero_thresholds.begin(), position.zero_thresholds.end(),
        [](double x) {return std::isfinite(x) && x >= 0.;})))
    {
      throw std::runtime_error("invalid wheel position parameters");
    }
    if (position_enabled_ && position.velocity_gated &&
      !std::all_of(position.velocity_thresholds.begin(), position.velocity_thresholds.end(),
        [](double x) {return std::isfinite(x) && x > 0.;}))
    {
      throw std::runtime_error("invalid wheel position velocity thresholds");
    }
    support_enabled_ = std::any_of(layout_.begin(), layout_.end(),
      [](const auto & e) {return e.kind == SupportMode;});
    pose_enabled_ = std::any_of(layout_.begin(), layout_.end(),
      [](const auto & e) {return e.kind == PoseCommands;});
    if (pose_enabled_) pose_cfg_.validate();
    if (pose_enabled_ && support_enabled_) throw std::runtime_error("pose and support commands cannot be combined");
  }

  void reset()
  {
    position_initialized_ = false;
    position_latched_ = false;
    heading_hold_ = 0;
    heading_ = 0.;
  }

  bool heading_enabled() const {return heading_enabled_;}
  bool support_enabled() const {return support_enabled_;}
  bool pose_enabled() const {return pose_enabled_;}
  // Gyro z bias [rad/s] subtracted before integration (robot: pre-RL stationary estimate).
  void set_gyro_bias(double bias)
  {
    if (!std::isfinite(bias)) throw std::runtime_error("non-finite gyro bias");
    gyro_bias_ = bias;
  }
  double gyro_bias() const {return gyro_bias_;}

  // heading_dt > 0 overrides the configured policy period for this call (robot: measured interval).
  std::vector<float> build(
    const RobotState & s, const std::array<double, 3> & command, const std::vector<float> & last_action,
    double heading_dt = -1.)
  {
    if (support_enabled_ && (s.support_mode < 0 || s.support_mode > 2)) {
      throw std::runtime_error("support mode must be 0, 1 or 2");
    }
    if (pose_enabled_) {
      for (std::size_t i = 0; i < 3; ++i) {
        // Match the float32 boundary comparisons in the sim2sim adapter.
        const float value = static_cast<float>(s.pose_command[i]);
        if (!std::isfinite(value) || value < static_cast<float>(pose_cfg_.low[i]) ||
          value > static_cast<float>(pose_cfg_.high[i]))
        {
          throw std::runtime_error("pose command outside trained range");
        }
      }
    }
    const auto gravity = projected_gravity(s.quat_wxyz);
    const double position_error = position_enabled_ ? wheel_position_error(s, command) : 0.;
    const double heading_error = heading_enabled_ ?
      gyro_heading_error(s, command, heading_dt > 0. ? heading_dt : heading_cfg_.dt) : 0.;
    std::vector<float> obs;
    obs.reserve(layout_.size());
    for (const auto & e : layout_) {
      double v = 0.;
      switch (e.kind) {
        case AngVel: v = s.ang_vel[e.index]; break;
        case Gravity: v = gravity[e.index]; break;
        case Command: v = command[e.index]; break;
        case JointPos: v = s.joint_pos[e.index] - default_pos_[e.index]; break;
        case JointVel: v = s.joint_vel[e.index] - default_vel_[e.index]; break;
        case LastAction: v = last_action[e.index]; break;
        case Zero: v = 0.; break;
        case WheelPositionError: v = position_error; break;
        case HeadingError: v = heading_error; break;
        case SupportMode: v = e.index == s.support_mode ? 1. : 0.; break;
        case PoseCommands: v = s.pose_command[e.index]; break;
        default: throw std::runtime_error("unknown observation kind");
      }
      const float value = static_cast<float>(std::clamp(v, e.low, e.high) * e.scale);
      if (!std::isfinite(value)) throw std::runtime_error("non-finite observation");
      obs.push_back(value);
    }
    return obs;
  }

private:
  double gyro_heading_error(const RobotState & s, const std::array<double, 3> & command, double dt)
  {
    if (!std::isfinite(s.ang_vel[2]) || !std::isfinite(dt) || dt <= 0.) {
      throw std::runtime_error("non-finite heading inputs");
    }
    bool zero = true;
    for (std::size_t i = 0; i < 3; ++i) {
      if (!std::isfinite(command[i])) throw std::runtime_error("non-finite command");
      zero &= std::abs(static_cast<float>(command[i])) <= static_cast<float>(heading_cfg_.zero_thresholds[i]);
    }
    heading_hold_ = zero ? heading_hold_ + 1 : 0;
    heading_ = zero && heading_hold_ > heading_warmup_steps_ ? heading_ + (s.ang_vel[2] - gyro_bias_) * dt : 0.;
    return std::clamp(heading_, -heading_cfg_.clip_rad, heading_cfg_.clip_rad);
  }

  double wheel_position_error(const RobotState & s, const std::array<double, 3> & command)
  {
    for (double x : s.joint_pos) {
      if (!std::isfinite(x)) throw std::runtime_error("non-finite wheel position inputs");
    }
    for (double x : s.quat_wxyz) {
      if (!std::isfinite(x)) throw std::runtime_error("non-finite wheel position inputs");
    }
    bool zero = true;
    for (std::size_t i = 0; i < 3; ++i) {
      if (!std::isfinite(command[i])) throw std::runtime_error("non-finite command");
      zero &= std::abs(static_cast<float>(command[i])) <= static_cast<float>(position_.zero_thresholds[i]);
    }
    const auto & q = s.quat_wxyz;
    const double pitch = std::asin(std::clamp(2. * (q[0] * q[2] - q[3] * q[1]), -1., 1.));
    double angle = 0.;
    for (std::size_t side = 0; side < 2; ++side) {
      const std::size_t j = side * 4;
      const double wheel = s.joint_pos[j + 3];
      if (!position_initialized_) {
        unwrapped_wheels_[side] = wheel;
      } else {
        const double delta = wheel - previous_wheels_[side];
        unwrapped_wheels_[side] += std::atan2(std::sin(delta), std::cos(delta));
      }
      previous_wheels_[side] = wheel;
      angle += unwrapped_wheels_[side] + pitch + s.joint_pos[j + 1] + s.joint_pos[j + 2];
    }
    const double distance = position_.radius * .5 * angle;
    if (!position_initialized_ || !zero) reference_ = distance;
    if (position_.velocity_gated) {
      if (!std::all_of(s.lin_vel_b.begin(), s.lin_vel_b.end(), [](double x) {return std::isfinite(x);}) ||
        !std::isfinite(s.ang_vel[2]))
      {
        throw std::runtime_error("velocity-gated wheel position requires finite body velocity");
      }
      const float vx = static_cast<float>(s.lin_vel_b[0]), vy = static_cast<float>(s.lin_vel_b[1]);
      const bool active = zero && std::sqrt(vx*vx + vy*vy) < position_.velocity_thresholds[0] &&
        std::abs(static_cast<float>(s.ang_vel[2])) < position_.velocity_thresholds[1];
      if (!active || !position_latched_) reference_ = distance;
      position_latched_ = active;
      zero = active;
    }
    if (position_.moving_anchor) {
      reference_ = std::clamp(reference_, distance - position_.clip_m, distance + position_.clip_m);
    }
    position_initialized_ = true;
    return zero ? std::clamp(distance - reference_, -position_.clip_m, position_.clip_m) : 0.;
  }

  std::vector<ObsElement> layout_;
  Joints default_pos_, default_vel_;
  WheelPositionConfig position_;
  bool position_enabled_{false}, position_initialized_{false};
  bool position_latched_{false}, support_enabled_{false};
  std::array<double, 2> previous_wheels_{}, unwrapped_wheels_{};
  double reference_{0.};
  HeadingConfig heading_cfg_;
  bool heading_enabled_{false};
  long heading_warmup_steps_{1}, heading_hold_{0};
  double heading_{0.}, gyro_bias_{0.};
  PoseCommandConfig pose_cfg_;
  bool pose_enabled_{false};
};

// Map policy order to native order, then apply position/velocity PD.
class ActionAdapter
{
public:
  ActionAdapter(std::vector<ActionTerm> terms, Joints kp, Joints kd, Joints limit)
  : terms_(std::move(terms)), kp_(kp), kd_(kd), limit_(limit) {}

  Joints compute(const std::vector<float> & action, const Joints & joint_pos, const Joints & joint_vel,
    const std::array<double, 2> & wheel_velocity_bias = {}, const Joints & residual = {}) const
  {
    Joints torque{};
    for (std::size_t i = 0; i < terms_.size(); ++i) {
      const auto & t = terms_[i];
      double target = std::clamp(action[i] * t.scale + t.offset, t.low, t.high);
      const int j = t.joint;
      if (t.velocity && (j == 3 || j == 7)) target += wheel_velocity_bias[j / 4];
      torque[j] = t.velocity ? kd_[j] * (target - joint_vel[j]) :
        kp_[j] * (target - joint_pos[j]) - kd_[j] * joint_vel[j];
      torque[j] = std::clamp(torque[j] + residual[j], -limit_[j], limit_[j]);
    }
    return torque;
  }

  // Logging only: clipped physical references in native joint order.
  void reference_targets(const std::vector<float> & action,
    const std::array<double, 2> & bias, Joints & q, Joints & v) const
  {
    q.fill(NAN); v = q;
    if (action.size() != terms_.size()) return;
    for (std::size_t i = 0; i < terms_.size(); ++i) {
      const auto & t = terms_[i];
      double target = std::clamp(action[i]*t.scale+t.offset, t.low, t.high);
      if (t.velocity && (t.joint == 3 || t.joint == 7)) target += bias[t.joint/4];
      if (t.velocity) v[t.joint] = target;
      else {q[t.joint] = target; v[t.joint] = 0.;}
    }
  }
  const Joints & kp() const {return kp_;}
  const Joints & kd() const {return kd_;}
  const Joints & effort_limits() const {return limit_;}

  // Logging only: equivalent policy-order ONNX outputs for corrected physical targets.
  // False means the adapter cannot reproduce at least one target (e.g. post-clip bias).
  // Export-time actor bounds are deliberately not assumed here; check them offline.
  bool teacher_action(const std::vector<float> & action,
    const std::array<double, 2> & wheel_velocity_bias, Joints & result) const
  {
    result.fill(0.);
    if (action.size() != 8 || terms_.size() != 8) return false;
    bool valid = true;
    for (std::size_t i = 0; i < terms_.size(); ++i) {
      const auto & t = terms_[i];
      if (!std::isfinite(t.scale) || t.scale == 0.) {valid = false; continue;}
      double target = std::clamp(action[i] * t.scale + t.offset, t.low, t.high);
      if (t.velocity && (t.joint == 3 || t.joint == 7)) {
        target += wheel_velocity_bias[t.joint / 4];
      }
      result[i] = (target - t.offset) / t.scale;
      valid &= std::isfinite(result[i]) && target >= t.low && target <= t.high;
    }
    return valid;
  }

private:
  std::vector<ActionTerm> terms_;
  Joints kp_, kd_, limit_;
};
}  // namespace tita
