// Four-second supporting sit validated in MuJoCo. Pure encoder/IMU math, no CAN sender.
#pragma once
#include <algorithm>
#include <array>
#include <cmath>
#include "tita_controller/sit_geometry.hpp"

namespace tita
{
using SitVector = std::array<double, 3>;
using SitQuaternion = std::array<double, 4>;
inline SitQuaternion sit_multiply(const SitQuaternion & a, const SitQuaternion & b)
{
  return {a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3],
    a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2],
    a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1],
    a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]};
}
inline SitVector sit_rotate(const SitQuaternion & q, const SitVector & v)
{
  const auto r = sit_multiply(sit_multiply(q, {0., v[0], v[1], v[2]}),
    {q[0], -q[1], -q[2], -q[3]});
  return {r[1], r[2], r[3]};
}
inline double sit_com_angle(const std::array<double, 8> & q, const SitQuaternion & imu)
{
  std::array<SitVector, 9> pos{};
  std::array<SitQuaternion, 9> rot{};
  SitVector com{};
  double mass = 0.;
  for (std::size_t i = 0; i < 9; ++i) {
    const auto & b = kSitBodies[i];
    if (i == 0) {rot[i] = imu;} else {
      const auto shift = sit_rotate(rot[b.parent], b.pos);
      for (int k = 0; k < 3; ++k) pos[i][k] = pos[b.parent][k] + shift[k];
      const double joint = q[i-1];  // Compiled nominal tree is base + native joint order.
      rot[i] = sit_multiply(sit_multiply(rot[b.parent], b.quat),
        {std::cos(joint/2.), 0., 0., std::sin(joint/2.)});
    }
    const auto c = sit_rotate(rot[i], b.com);
    for (int k = 0; k < 3; ++k) com[k] += b.mass * (pos[i][k] + c[k]);
    mass += b.mass;
  }
  for (int k = 0; k < 3; ++k) com[k] = com[k]/mass - .5*(pos[4][k]+pos[8][k]);
  const double yaw = std::atan2(2.*(imu[0]*imu[3]+imu[1]*imu[2]),
    1.-2.*(imu[2]*imu[2]+imu[3]*imu[3]));
  return std::atan2(com[0]*std::cos(yaw)+com[1]*std::sin(yaw), com[2]);
}

class SupportingSit
{
public:
  static constexpr double kSeconds = 4.;
  using Eight = std::array<double, 8>;
  void start(const Eight & q, const Eight & dq, const Eight & previous,
    const SitQuaternion & imu, const SitVector & gyro)
  {
    start_ = q;
    for (std::size_t i = 0; i < 8; ++i) {
      if (i != 3 && i != 7) start_[i] += (previous[i]+kd_[i]*dq[i])/kp_[i];
    }
    wheel_start_ = {dq[3]+previous[3]/.5, dq[7]+previous[7]/.5};
    angle_start_ = sit_com_angle(q, imu);
    initial_ = 5.*gyro[1] + .5*(dq[3]-wheel_start_[0]+dq[7]-wheel_start_[1]);
  }
  Eight torque(const Eight & q, const Eight & dq, double elapsed,
    const SitQuaternion & imu, const SitVector & gyro, const Eight & limits) const
  {
    const double t = std::clamp(elapsed/kSeconds, 0., 1.);
    const double a = t*t*(3.-2.*t);
    Eight tau{};
    for (std::size_t i = 0; i < 8; ++i) {
      double ref = start_[i]+a*(goal_[i]-start_[i]);
      if (i == 1 || i == 5) ref += .3*std::sin(3.14159265358979323846*a);
      tau[i] = kp_[i]*(ref-q[i])-kd_[i]*dq[i];
    }
    const double fold = std::clamp((-.5*(q[2]+q[6])-2.35)/.30, 0., 1.);
    const double blend = 1.-fold*fold*(3.-2.*fold);
    const double balance = 30.*(sit_com_angle(q, imu)-(1.-a)*angle_start_) + 5.*gyro[1] +
      .5*(dq[3]-(1.-a)*wheel_start_[0]+dq[7]-(1.-a)*wheel_start_[1]);
    for (int j = 0; j < 2; ++j) {
      const int i = j == 0 ? 3 : 7;
      tau[i] = .5*((1.-a)*wheel_start_[j]-dq[i]) + blend*(balance-(1.-a)*initial_);
    }
    for (std::size_t i = 0; i < 8; ++i) tau[i] = std::clamp(tau[i], -limits[i], limits[i]);
    return tau;
  }
private:
  const Eight kp_{600., 80., 80., 0., 600., 80., 80., 0.};
  const Eight kd_{8., 8., 8., .5, 8., 8., 8., .5};
  // Effective native sit target, with original feedforward absorbed into q_ref.
  const Eight goal_{-.05-20./600., .9, -2.6-25./80., 0., .05+20./600., .9, -2.6-25./80., 0.};
  Eight start_{};
  std::array<double, 2> wheel_start_{};
  double angle_start_{0.}, initial_{0.};
};
}  // namespace tita
