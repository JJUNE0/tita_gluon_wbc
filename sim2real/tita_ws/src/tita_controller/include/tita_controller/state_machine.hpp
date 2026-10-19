// Startup idle -> transform_up -> sit -> rl; RL exit returns smoothly to sit.
// A valid upright software stop supports a slow sit; sensor/fall faults use damping.
#pragma once

#include <algorithm>
#include <array>
#include <cmath>
#include <string>
#include "tita_controller/supporting_sit.hpp"

namespace tita
{
using Joints = std::array<double, 8>;  // native order: left leg_1..4, right leg_1..4

// leg_1 axes are parallel, so mirrored poses flip its sign.
constexpr Joints kSplayPose{0.75, 1.2, -2.7, 0., -0.75, 1.2, -2.7, 0.};
constexpr Joints kSitPose{-0.05, 0.9, -2.6, 0., 0.05, 0.9, -2.6, 0.};
// Reference PD from the former transform_up; wheels only get velocity damping.
constexpr Joints kKp{600., 80., 80., 0., 600., 80., 80., 0.};
constexpr Joints kKd{8., 8., 8., .5, 8., 8., 8., .5};
constexpr Joints kFf{-20., 0., -25., 0., 20., 0., -25., 0.};
constexpr double kSplaySecondsPerRad = 4.;
constexpr double kSitSeconds = 2.;
constexpr double kSettleSeconds = .2;

enum class State { Idle, Damp, TransformUp, Sit, Rl, ReturnToSit, EStop };

inline const char * name(State state)
{
  switch (state) {
    case State::Idle: return "idle";
    case State::Damp: return "damp";
    case State::TransformUp: return "transform_up";
    case State::Sit: return "sit";
    case State::Rl: return "rl";
    case State::ReturnToSit: return "return_to_sit";
    case State::EStop: return "estop";
  }
  return "?";
}

class StateMachine
{
public:
  explicit StateMachine(const Joints & torque_limit) : limit_(torque_limit) {}

  State state() const {return state_;}

  // Called once per motor tick, before button/fault requests.
  void observe(const Joints & q, const Joints & dq, const SitQuaternion & imu,
    const SitVector & gyro, bool valid = true)
  {
    sensor_q_ = q; sensor_dq_ = dq; sensor_imu_ = imu; sensor_gyro_ = gyro;
    sensors_valid_ = valid;
  }

  // Software stop remains latched until this state machine is recreated.
  bool request(State state, const Joints & joint_pos, const Joints & previous_torque = Joints{})
  {
    // A hard fault cancels the supporting controller, even during a latched stop.
    // The latch itself survives: no later request may resume RL.
    if (state == State::Damp) supporting_ = false;
    if (state_ == State::EStop) return state == State::EStop;
    if (state == State::Rl && state_ != State::Sit) return false;
    if (state == State::ReturnToSit && state_ != State::Rl) return false;
    if (state == State::ReturnToSit && !sensors_valid_) return false;
    if (state == State::ReturnToSit ||
      (state == State::EStop && sensors_valid_ &&
      (state_ == State::Rl || state_ == State::Sit || state_ == State::ReturnToSit)))
    {
      if (!supporting_) {
        supporting_sit_.start(joint_pos, sensor_dq_, previous_torque, sensor_imu_, sensor_gyro_);
        elapsed_ = 0.;
        supporting_ = true;
      }
    } else if (state != State::EStop) {
      supporting_ = false;
    }
    if (state == State::TransformUp) {
      start_ = joint_pos;
      target_ = joint_pos;
      elapsed_ = 0.;
    }
    state_ = state;
    return true;
  }

  void update(double dt)
  {
    if (supporting_) {
      elapsed_ += dt;
      if (state_ == State::ReturnToSit && elapsed_ >= SupportingSit::kSeconds) state_ = State::Sit;
      return;
    }
    if (state_ != State::TransformUp) return;
    elapsed_ += dt;
    double max_error = 0.;
    for (std::size_t i = 0; i < 8; ++i) max_error = std::max(max_error, std::abs(start_[i] - kSplayPose[i]));
    const double splay_time = std::max(kSplaySecondsPerRad * max_error, 1e-6);
    const double t = elapsed_;
    for (std::size_t i = 0; i < 8; ++i) {
      target_[i] = t < splay_time ?
        start_[i] + (kSplayPose[i] - start_[i]) * (t / splay_time) :
        kSplayPose[i] + (kSitPose[i] - kSplayPose[i]) * std::min((t - splay_time) / kSitSeconds, 1.);
    }
    if (t >= splay_time + kSitSeconds + kSettleSeconds) state_ = State::Sit;
  }

  // Torque for every state except rl (the policy owns rl).
  Joints torque(const Joints & joint_pos, const Joints & joint_vel) const
  {
    if (supporting_) {
      return supporting_sit_.torque(joint_pos, joint_vel, elapsed_, sensor_imu_, sensor_gyro_, limit_);
    }
    Joints torque{};
    for (std::size_t i = 0; i < 8; ++i) {
      torque[i] = (state_ == State::Idle || state_ == State::Damp || state_ == State::EStop) ? -kKd[i] * joint_vel[i] :
        kKp[i] * (target_[i] - joint_pos[i]) - kKd[i] * joint_vel[i] + kFf[i];
      torque[i] = std::clamp(torque[i], -limit_[i], limit_[i]);
    }
    return torque;
  }

private:
  SupportingSit supporting_sit_;
  bool supporting_{false}, sensors_valid_{false};
  Joints sensor_q_{}, sensor_dq_{};
  SitQuaternion sensor_imu_{1., 0., 0., 0.};
  SitVector sensor_gyro_{};
  Joints limit_;
  State state_{State::Idle};
  Joints start_{};
  Joints target_{kSitPose};
  double elapsed_{0.};
};
}  // namespace tita
