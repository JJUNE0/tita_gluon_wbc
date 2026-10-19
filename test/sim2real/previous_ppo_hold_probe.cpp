// DESKTOP_DRY_RUN: previous core SAFE_HOLD under ideal sensor tracking; no SDK/ROS.
#include <cassert>
#include <cmath>
#include <iostream>
#include "tita_stage1_controller/stage1_core.hpp"

int main()
{
  using namespace tita_stage1_controller;
  Stage1Config cfg;
  cfg.fold_jpos = {.75, 1.2, -2.7, 0., -.75, 1.2, -2.7, 0.};
  cfg.stand_jpos = {-.05, .9, -2.6, 0., .05, .9, -2.6, 0.};
  cfg.transform_kp = {600., 80., 80., 5., 600., 80., 80., 5.};
  cfg.transform_kd = {8., 8., 8., .5, 8., 8., 8., .5};
  cfg.ff_effort = {-20., 0., -25., 0., 20., 0., -25., 0.};
  cfg.transition_lower_limits = {-.785398, -1.919862, -2.7, -62831.85, -.785398, -1.919862, -2.7, -62831.85};
  cfg.transition_upper_limits = {.785398, 3.490659, -.698132, 62831.85, .785398, 3.490659, -.698132, 62831.85};
  cfg.lower_limits = cfg.transition_lower_limits;
  cfg.lower_limits[2] = cfg.lower_limits[6] = -2.670354;
  cfg.upper_limits = cfg.transition_upper_limits;
  cfg.effort_limits = {60., 60., 60., 12., 60., 60., 60., 12.};
  cfg.rl_kp = {60., 60., 60., 0., 60., 60., 60., 0.};
  cfg.rl_kd = {1.5, 1.5, 1.5, .5, 1.5, 1.5, 1.5, .5};
  cfg.stage2_enabled = true;
  cfg.rl_running_seconds = 0.;
  cfg.require_zero_joystick = false;
  cfg.operational_entry_margin_rad = .019;
  Stage1Core core(cfg);
  assert(core.valid_config() && core.command_envelopes_valid());
  core.activate();
  Stage1Input input;
  input.q = cfg.stand_jpos;
  input.hardware_read_valid = input.motors_online = input.hardware_output_enabled = true;
  input.period_seconds = .002;
  input.joystick_fresh = input.joystick_zero = input.observation_valid = true;
  input.inference_valid = input.inference_deadline_ok = input.rl_target_delta_ok = true;
  input.rl_mixed_target = cfg.stand_jpos;
  input.rl_mixed_target[0] += .1;
  input.rl_mixed_target[4] -= .1;
  input.rl_mixed_target[3] = input.rl_mixed_target[7] = 2.;
  Stage1Output output;
  for (int i = 0; i < 15000 && core.state() != Stage1State::RL_RUNNING; ++i) {
    output = core.update(input);
    if (output.command_enable) input.q = output.q;
    assert(output.state != Stage1State::FAULT && output.state != Stage1State::SAFE_HOLD);
  }
  assert(core.state() == Stage1State::RL_RUNNING);
  const auto previous_q = output.q;
  const auto previous_v = output.v;
  core.request_safe_hold("OPERATOR_SAFE_HOLD");
  output = core.update(input);
  assert(output.state == Stage1State::SAFE_HOLD && output.command_enable);
  assert(output.kp[0] == 600. && output.kp[2] == 80. && output.kd[2] == 8.);
  assert(output.effort == JointArray{});
  assert(std::abs(output.q[0] - previous_q[0] + .003) < 1e-10);
  assert(std::abs(output.v[3] - previous_v[3] + .01) < 1e-10);
  std::cout << "SAFE_HOLD first tick: leg Kp=" << output.kp[0] << '/' << output.kp[2]
            << "; leg Kd=" << output.kd[2] << "; feedforward=0; hip target step="
            << output.q[0]-previous_q[0] << " rad; wheel target=" << previous_v[3]
            << " -> " << output.v[3] << " rad/s\n";
  for (int i = 0; i < 250; ++i) {
    input.q = output.q;
    output = core.update(input);
    assert(output.state == Stage1State::SAFE_HOLD);
    assert(output.kp[2] == 80. && output.kd[2] == 8.);
  }
  assert(std::abs(output.v[3]) < 1e-10);
  assert(output.q[0] == cfg.stand_jpos[0]);
  std::cout << "PASS: archived-identical previous core keeps full leg PD, slews pose at 1.5 rad/s, "
            << "brakes wheel target at 5 rad/s^2 and stays latched; ideal tracking only\n";
}
