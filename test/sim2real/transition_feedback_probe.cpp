// DESKTOP_DRY_RUN: probe actual state-machine feedback; no ROS, SDK or CAN.
#include <cassert>
#include <cmath>
#include <iomanip>
#include <iostream>
#include "tita_controller/state_machine.hpp"

int main()
{
  using namespace tita;
  const Joints limits{60., 60., 60., 12., 60., 60., 60., 12.};
  const Joints pose{0., .8, -1.5, 0., 0., .8, -1.5, 0.};
  // Synthetic example to expose retention of a single wheel-torque sample.
  const Joints previous{8., 5., -10., 3., -8., 5., -10., 3.};
  constexpr double eps = 1e-5;
  std::cout << std::setprecision(12);
  std::cout << "time_s,alpha,leg1_kp,leg3_kp,leg3_kd,wheel_kd,retained_example_wheel_nm\n";
  for (double time : {0., .002, .1, .2, .5, 1., 1.5, 2.}) {
    StateMachine sm(limits);
    assert(sm.request(State::TransformUp, kSitPose));
    sm.update(20.);
    assert(sm.state() == State::Sit);
    assert(sm.request(State::Rl, pose));
    assert(sm.request(State::ReturnToSit, pose, previous));
    if (time == 0.) assert(sm.torque(pose, Joints{}) == previous);
    sm.update(time);
    const double phase = time / 2.;
    const double alpha = phase * phase * (3. - 2. * phase);
    Joints reference{};
    for (std::size_t j = 0; j < 8; ++j) reference[j] = pose[j] + alpha * (kSitPose[j] - pose[j]);
    auto q0 = reference, q2 = reference;
    q0[0] += eps;
    q2[2] += eps;
    Joints v2{}, v3{};
    v2[2] = eps;
    v3[3] = eps;
    const auto base = sm.torque(reference, Joints{});
    const double kp0 = (base[0] - sm.torque(q0, Joints{})[0]) / eps;
    const double kp2 = (base[2] - sm.torque(q2, Joints{})[2]) / eps;
    const double kd2 = (base[2] - sm.torque(reference, v2)[2]) / eps;
    const double kd3 = (base[3] - sm.torque(reference, v3)[3]) / eps;
    assert(std::abs(kp0 - alpha * 600.) < 1e-7);
    assert(std::abs(kp2 - alpha * 80.) < 1e-7);
    assert(std::abs(kd2 - alpha * 8.) < 1e-7);
    assert(std::abs(kd3 - alpha * .5) < 1e-7);
    assert(std::abs(base[3] - (1.-alpha)*3.) < 1e-10);
    std::cout << time << ',' << alpha << ',' << kp0 << ',' << kp2 << ','
              << kd2 << ',' << kd3 << ',' << base[3] << '\n';
  }
  StateMachine stopped(limits);
  stopped.request(State::EStop, pose);
  assert(stopped.torque(pose, Joints{}) == Joints{});
  Joints other = pose;
  other[2] += .1;
  assert(stopped.torque(other, Joints{}) == Joints{});
  Joints velocity{};
  velocity[2] = 1.;
  assert(stopped.torque(pose, velocity)[2] == -8.);
  assert(!stopped.request(State::Rl, pose));
  std::cerr << "PASS: actual-header feedback derivatives, frozen wheel-torque blend, "
            << "entry torque continuity and zero static EStop support\n";
}
