// Observation layout and native joint PD. C++ port of sim2sim adapter.py.
// The launch file flattens the checkpoint config.json into one entry per observation element
// and per action, so this file only loops.
#pragma once

#include <algorithm>
#include <array>
#include <stdexcept>
#include <vector>

#include "tita_controller/state_machine.hpp"

namespace tita
{
// Observation element sources (must match OBS_KINDS in launch/tita.launch.py).
enum ObsKind { AngVel, Gravity, Command, JointPos, JointVel, LastAction, Zero };

struct ObsElement { int kind; int index; double scale, low, high; };
struct ActionTerm { int joint; bool velocity; double scale, offset, low, high; };

struct RobotState
{
  Joints joint_pos{}, joint_vel{};
  std::array<double, 4> quat_wxyz{1., 0., 0., 0.};
  std::array<double, 3> ang_vel{};
};

// R(q)^T [0, 0, -1]
inline std::array<double, 3> projected_gravity(const std::array<double, 4> & q)
{
  const double w = q[0], x = q[1], y = q[2], z = q[3];
  return {-2. * (x * z - w * y), -2. * (y * z + w * x), -(1. - 2. * (x * x + y * y))};
}

class ObservationBuilder
{
public:
  ObservationBuilder(std::vector<ObsElement> layout, Joints default_pos, Joints default_vel)
  : layout_(std::move(layout)), default_pos_(default_pos), default_vel_(default_vel) {}

  std::vector<float> build(
    const RobotState & s, const std::array<double, 3> & command, const std::vector<float> & last_action) const
  {
    const auto gravity = projected_gravity(s.quat_wxyz);
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
        default: throw std::runtime_error("unknown observation kind");
      }
      const float value = static_cast<float>(std::clamp(v, e.low, e.high) * e.scale);
      if (!std::isfinite(value)) throw std::runtime_error("non-finite observation");
      obs.push_back(value);
    }
    return obs;
  }

private:
  std::vector<ObsElement> layout_;
  Joints default_pos_, default_vel_;
};

// Map policy order to native order, then apply position/velocity PD.
class ActionAdapter
{
public:
  ActionAdapter(std::vector<ActionTerm> terms, Joints kp, Joints kd, Joints limit)
  : terms_(std::move(terms)), kp_(kp), kd_(kd), limit_(limit) {}

  Joints compute(const std::vector<float> & action, const Joints & joint_pos, const Joints & joint_vel,
    const std::array<double, 2> & wheel_velocity_bias = {}) const
  {
    Joints torque{};
    for (std::size_t i = 0; i < terms_.size(); ++i) {
      const auto & t = terms_[i];
      double target = std::clamp(action[i] * t.scale + t.offset, t.low, t.high);
      const int j = t.joint;
      if (t.velocity && (j == 3 || j == 7)) target += wheel_velocity_bias[j / 4];
      torque[j] = t.velocity ? kd_[j] * (target - joint_vel[j]) :
        kp_[j] * (target - joint_pos[j]) - kd_[j] * joint_vel[j];
      torque[j] = std::clamp(torque[j], -limit_[j], limit_[j]);
    }
    return torque;
  }

private:
  std::vector<ActionTerm> terms_;
  Joints kp_, kd_, limit_;
};
}  // namespace tita
