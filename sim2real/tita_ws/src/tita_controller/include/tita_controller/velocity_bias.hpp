// IMU/encoder/FK velocity bias with a real-robot correction torque bound.
// No base position/velocity, new CAN sender, RLS or policy modification.
#pragma once

#include <Eigen/Geometry>
#include <algorithm>
#include <array>
#include <cmath>
#include <stdexcept>
#include <vector>

#include "tita_controller/adapter.hpp"

namespace tita
{
class VelocityBiasLaw
{
public:
  VelocityBiasLaw(double limit, double slew, double response_sign)
  : limit_(limit), slew_(slew), sign_(response_sign)
  {
    if (!std::isfinite(limit) || !std::isfinite(slew) || limit <= 0. || slew <= 0. ||
      (response_sign != 1. && response_sign != -1.))
    {
      throw std::runtime_error("invalid velocity bias limit/slew/response sign");
    }
  }

  void reset() {filtered = integral = bias = age = 0.;}

  double update(double velocity, double dt, bool enabled)
  {
    if (!std::isfinite(velocity) || !std::isfinite(dt) || dt <= 0.) {
      throw std::runtime_error("invalid velocity bias sample");
    }
    double desired = 0.;
    if (enabled) {
      filtered += (1. - std::exp(-dt / std::max(.1, dt))) * (velocity - filtered);
      const double phase = std::min(age / 1., 1.);
      const double bound = limit_ * phase * phase * (3. - 2. * phase);
      desired = std::clamp(integral + sign_ * 4. * filtered * dt, -bound, bound);
      age += dt;
    } else {
      reset();
      return bias;
    }
    bias = std::clamp(desired, bias - slew_ * dt, bias + slew_ * dt);
    integral = bias;  // Track the bounded/rate-limited output: no hidden windup.
    return bias;
  }

  double filtered{0.}, integral{0.}, bias{0.}, age{0.};

private:
  double limit_, slew_, sign_;
};

class WheelVelocityBias
{
public:
  static constexpr double kMaxTorque = .8;  // N*m per wheel, additional to baseline PD.
  static constexpr double kIgnore = 1.;
  static constexpr double kApply = 3.;
  static constexpr double kPitchDeviation = .08726646259971647;  // 5 degrees from acquisition mean.

  WheelVelocityBias(const std::vector<double> & xyz, const std::vector<double> & rpy,
    const std::vector<double> & axes, double radius, double response_sign,
    const std::array<double, 2> & wheel_kd = {.5, .5})
  : radius_(radius), law_(bias_limit(radius, wheel_kd), bias_limit(radius, wheel_kd), response_sign)
  {
    if (xyz.size() != 24 || rpy.size() != 24 || axes.size() != 24 ||
      !std::isfinite(radius) || radius <= 0.)
    {
      throw std::runtime_error("invalid velocity bias geometry/radius");
    }
    for (std::size_t i = 0; i < 8; ++i) {
      origin_[i] = Eigen::Isometry3d::Identity();
      origin_[i].translation() = Eigen::Vector3d(xyz[3*i], xyz[3*i+1], xyz[3*i+2]);
      origin_[i].linear() = (
        Eigen::AngleAxisd(rpy[3*i+2], Eigen::Vector3d::UnitZ()) *
        Eigen::AngleAxisd(rpy[3*i+1], Eigen::Vector3d::UnitY()) *
        Eigen::AngleAxisd(rpy[3*i], Eigen::Vector3d::UnitX())).toRotationMatrix();
      axes_[i] = Eigen::Vector3d(axes[3*i], axes[3*i+1], axes[3*i+2]);
      if (!origin_[i].matrix().allFinite() || !axes_[i].allFinite() ||
        std::abs(axes_[i].norm() - 1.) > 1e-6)
      {
        throw std::runtime_error("non-finite velocity bias geometry or non-unit joint axis");
      }
    }
  }

  void reset()
  {
    holding_ = eligible_ = have_offset_ = acquired_ = inhibited_ = false;
    velocity_ = age_ = u_ = 0.;
    velocity_sum_ = pitch_sum_ = acquisition_time_ = pitch_reference_ = 0.;
    signs_ = {0., 0.};
    law_.reset();
  }

  void update(const RobotState & s, const std::array<double, 3> & command, double dt)
  {
    if (!std::isfinite(dt) || dt <= 0. || dt > .06) {reset(); return;}
    const std::array<double, 3> enter{.02, .02, .03}, leave{.04, .04, .06};
    bool low = true, high = false;
    for (std::size_t i = 0; i < 3; ++i) {
      if (!std::isfinite(command[i])) {reset(); return;}
      low &= std::abs(command[i]) <= enter[i];
      high |= std::abs(command[i]) >= leave[i];
    }
    if (!holding_ && low) {holding_ = true; age_ = 0.; have_offset_ = false;}
    else if (holding_ && high) {reset(); return;}
    double target = 0.;
    eligible_ = false;
    if (holding_) {
      const Eigen::Quaterniond quat(s.quat_wxyz[0], s.quat_wxyz[1], s.quat_wxyz[2], s.quat_wxyz[3]);
      if (!quat.coeffs().allFinite() || std::abs(quat.norm() - 1.) > .01) {
        throw std::runtime_error("invalid velocity observer IMU quaternion");
      }
      const Eigen::Matrix3d rotation = quat.toRotationMatrix();
      const double yaw = std::atan2(rotation(1, 0), rotation(0, 0));
      const double pitch = std::asin(std::clamp(-rotation(2, 0), -1., 1.));
      const double roll = std::atan2(rotation(2, 1), rotation(2, 2));
      const Eigen::Vector3d lateral(-std::sin(yaw), std::cos(yaw), 0.);
      const Eigen::Vector3d forward(std::cos(yaw), std::sin(yaw), 0.);
      const Eigen::Vector3d gyro(s.ang_vel[0], s.ang_vel[1], s.ang_vel[2]);
      double sum_rates = 2. * lateral.dot(rotation * gyro);
      Eigen::Vector3d offset = Eigen::Vector3d::Zero();
      for (std::size_t side = 0; side < 2; ++side) {
        Eigen::Isometry3d frame = Eigen::Isometry3d::Identity();
        frame.linear() = rotation;
        for (std::size_t j = side * 4; j < side * 4 + 4; ++j) {
          if (!std::isfinite(s.joint_pos[j]) || !std::isfinite(s.joint_vel[j])) {
            throw std::runtime_error("non-finite velocity observer encoder");
          }
          frame = frame * origin_[j];
          const double projection = lateral.dot(frame.linear() * axes_[j]);
          sum_rates += projection * s.joint_vel[j];
          if (j % 4 == 3) signs_[side] = projection >= 0. ? 1. : -1.;
          frame.rotate(Eigen::AngleAxisd(s.joint_pos[j], axes_[j]));
        }
        offset += frame.translation() / 2.;
      }
      velocity_ = radius_ * sum_rates / 2.;
      if (have_offset_) velocity_ -= (offset - previous_offset_).dot(forward) / dt;
      previous_offset_ = offset;
      have_offset_ = true;
      if (!std::isfinite(velocity_)) throw std::runtime_error("non-finite velocity estimate");
      const bool safe = std::max(std::abs(roll), std::abs(pitch)) <= .3 && std::abs(velocity_) <= 1.;
      if (age_ + 1e-9 >= kIgnore && age_ + 1e-9 < kApply && !inhibited_) {
        if (!safe) {
          inhibited_ = true;
        } else {
          acquisition_time_ += dt;
          velocity_sum_ += velocity_ * dt;
          pitch_sum_ += pitch * dt;
          law_.filtered = velocity_sum_ / acquisition_time_;  // Velocity estimate, never a torque seed.
          pitch_reference_ = pitch_sum_ / acquisition_time_;
        }
      }
      if (age_ + 1e-9 >= kApply && !inhibited_) {
        acquired_ = acquisition_time_ >= 1.8;
        if (!acquired_ || !safe || std::abs(pitch - pitch_reference_) > kPitchDeviation) {
          inhibited_ = true;  // Do not reacquire a shifted posture until command exit or RL reset.
        } else {
          eligible_ = true;
          target = law_.update(velocity_, dt, true);
        }
      }
      if (inhibited_) law_.reset();
      age_ += dt;
    } else {
      law_.reset();
      have_offset_ = false;
      age_ = velocity_ = 0.;
    }
    u_ = target;  // Law already applies ramp/slew; exits and guards cut correction immediately.
  }

  bool acquired() const {return acquired_;}
  bool inhibited() const {return inhibited_;}
  double estimated_drift() const {return acquisition_time_ > 0. ? velocity_sum_ / acquisition_time_ : 0.;}
  double pitch_reference() const {return pitch_reference_;}

  std::array<double, 2> wheel_offsets() const
  {
    return {signs_[0] * u_ / radius_, signs_[1] * u_ / radius_};
  }

  // holding, eligible, hold_age_s, v_hat, LPF_v, integral, bias_m_s, dq_bias_L/R
  std::vector<float> diagnostics() const
  {
    const auto offsets = wheel_offsets();
    return {static_cast<float>(holding_), static_cast<float>(eligible_), static_cast<float>(age_),
      static_cast<float>(velocity_), static_cast<float>(law_.filtered), static_cast<float>(law_.integral),
      static_cast<float>(u_), static_cast<float>(offsets[0]), static_cast<float>(offsets[1])};
  }

private:
  static double bias_limit(double radius, const std::array<double, 2> & kd)
  {
    if (!std::isfinite(radius) || radius <= 0. || !std::isfinite(kd[0]) || !std::isfinite(kd[1]) ||
      kd[0] <= 0. || kd[1] <= 0.) throw std::runtime_error("invalid wheel radius/Kd for torque bound");
    // Clipping the final effort cannot increase this additional-torque difference.
    return kMaxTorque * radius / std::max(kd[0], kd[1]);
  }

  double radius_;
  VelocityBiasLaw law_;
  std::array<Eigen::Isometry3d, 8> origin_;
  std::array<Eigen::Vector3d, 8> axes_;
  Eigen::Vector3d previous_offset_{Eigen::Vector3d::Zero()};
  std::array<double, 2> signs_{0., 0.};
  bool holding_{false}, eligible_{false}, have_offset_{false}, acquired_{false}, inhibited_{false};
  double velocity_{0.}, age_{0.}, u_{0.};
  double velocity_sum_{0.}, pitch_sum_{0.}, acquisition_time_{0.}, pitch_reference_{0.};
};
}  // namespace tita
