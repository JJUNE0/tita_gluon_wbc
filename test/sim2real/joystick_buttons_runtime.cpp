// DESKTOP_DRY_RUN: real button/state headers only; no ROS, CAN or robot SDK.
#include <cmath>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

#include "tita_controller/joystick_buttons.hpp"
#include "tita_controller/state_machine.hpp"

using namespace tita;
const Joints limits{60., 60., 60., 12., 60., 60., 60., 12.};

void require(bool value, const char * message)
{
  if (!value) throw std::runtime_error(message);
}

void reach_rl(StateMachine & sm)
{
  require(sm.request(State::TransformUp, kSplayPose), "start transform");
  for (int i = 0; i < 1200; ++i) sm.update(.002);
  require(sm.state() == State::Sit, "transform completes in sit");
  require(sm.request(State::Rl, kSitPose), "sit allows RL");
  sm.observe(kSitPose, Joints{}, {1., 0., 0., 0.}, {});
}

void decoding()
{
  require(button_down(-1.).value() && !button_down(1.).value(), "down/up decoding");
  require(!button_down(0.) && !button_down(.49), "middle must not count as up/down");
  require(!button_down(std::numeric_limits<double>::quiet_NaN()), "NaN rejected");
  require(!button_down(std::numeric_limits<double>::infinity()), "infinity rejected");
  require(!button_down(2.), "out-of-range rejected");
}

void startup_interlock()
{
  for (bool left : {false, true}) {
    for (bool right : {false, true}) {
      JoystickButtons b;
      require(b.update(true, left, right, 0.) == ButtonEvent::None, "startup ignored");
      require(b.update(true, left, right, 2.) == ButtonEvent::None, "startup hold ignored");
      require(b.update(true, false, false, 3.) == ButtonEvent::None, "both release arms");
      require(b.update(true, false, true, 4.) == ButtonEvent::None, "right press begins hold");
      require(b.update(true, false, true, 4.999) == ButtonEvent::None, "sub-second hold cannot start");
      require(b.update(true, false, true, 5.) == ButtonEvent::TransformUp, "one-second hold starts");
    }
  }
  JoystickButtons b;
  b.update(true, false, false, 0.);
  require(b.update(true, true, true, 1.) == ButtonEvent::None, "simultaneous start cannot skip preparation");
  require(b.update(true, false, true, 3.) == ButtonEvent::None, "left release cannot start while right held");
  b.update(true, false, false, 4.);
  b.update(true, false, true, 5.);
  require(b.update(true, false, true, 6.) == ButtonEvent::TransformUp, "release then hold works");
}

void start_buttons(JoystickButtons & b)
{
  b.update(true, false, false, 0.);
  require(b.update(true, false, true, 1.) == ButtonEvent::None, "start hold");
  require(b.update(true, false, true, 2.) == ButtonEvent::TransformUp, "complete hold");
}

void short_hold_cancels()
{
  JoystickButtons b;
  b.update(true, false, false, 0.);
  b.update(true, false, true, 1.);
  require(b.update(true, false, false, 1.9) == ButtonEvent::None, "short release cancels");
  require(b.update(true, false, false, 3.) == ButtonEvent::None, "released cannot finish old hold");
  b.update(true, false, true, 4.);
  require(b.update(true, false, true, 4.99) == ButtonEvent::None, "hold restarts from zero");
  require(b.update(true, false, true, 5.) == ButtonEvent::TransformUp, "second full hold works");
}

void expected_edges()
{
  JoystickButtons b;
  start_buttons(b);
  for (int i = 0; i < 100; ++i) require(b.update(true, false, true, 2.01 + i * .01) == ButtonEvent::None, "startup hold cannot stop");
  require(b.update(true, false, false, 4.) == ButtonEvent::None, "startup release is harmless");
  require(b.update(true, true, false, 5.) == ButtonEvent::Rl, "left down selects RL");
  require(b.update(true, true, false, 6.) == ButtonEvent::None, "left hold does not toggle RL off");
  require(b.update(true, false, false, 7.) == ButtonEvent::ReturnToSit, "left up returns to sit");
  require(b.update(true, false, true, 8.) == ButtonEvent::Stop, "new right press stops immediately");
  b.update(true, false, false, 9.);
  require(b.update(true, false, true, 10.) == ButtonEvent::None, "stop cannot rearm");
  require(b.update(true, true, true, 11.) == ButtonEvent::None, "stop cannot enter RL");
}

void early_left_press()
{
  StateMachine sm(limits);
  JoystickButtons b;
  start_buttons(b);
  sm.request(State::TransformUp, kSplayPose);
  require(b.update(true, true, true, 3.) == ButtonEvent::Rl, "early left edge");
  require(!sm.request(State::Rl, kSplayPose), "early RL rejected");
  sm.update(3.);
  require(sm.state() == State::Sit, "preparation finished");
  require(b.update(true, true, true, 4.) == ButtonEvent::None, "held early selection does not queue RL");
  b.update(true, false, true, 5.);
  require(b.update(true, true, true, 6.) == ButtonEvent::Rl, "new press required");
  require(sm.request(State::Rl, kSitPose), "new RL request succeeds");
}

void return_trajectory()
{
  // Wide limit permits checking direction without saturation obscuring the result.
  StateMachine sm(Joints{200., 200., 200., 20., 200., 200., 200., 20.});
  reach_rl(sm);
  Joints pose = kSitPose;
  pose[0] = .4;  // Sit lies below this value; splay lies above it.
  const Joints previous{7., -3., 2., 1., -5., 4., -2., -1.};
  require(sm.request(State::ReturnToSit, pose, previous), "RL return accepted");
  for (int i = 0; i < 8; ++i) require(std::abs(sm.torque(pose, Joints{})[i]-previous[i]) < 1e-10, "return begins at previous torque");
  sm.update(2.);
  const auto middle = sm.torque(pose, Joints{});
  require(middle[0] < 0., "return goes directly toward sit, not toward splay");
  require(!sm.request(State::Rl, pose), "RL rejected during return");
  sm.update(2.01);
  require(sm.state() == State::Sit, "return completes in sit");
  require(std::abs(sm.torque(kSitPose, Joints{})[2] - kFf[2]) < 1e-10, "sit holds original target and feedforward");
  require(sm.request(State::Rl, kSitPose), "can enter RL again after return");
}

void return_limits()
{
  StateMachine sm(limits);
  require(!sm.request(State::ReturnToSit, kSitPose), "idle cannot request RL return");
  reach_rl(sm);
  Joints pose = kSitPose;
  pose[0] += 1.;
  sm.request(State::ReturnToSit, pose, Joints{100., -100., 100., -100., 100., -100., 100., -100.});
  for (int tick = 0; tick < 1200; ++tick) {
    sm.update(.002);
    const auto torque = sm.torque(pose, Joints{20., -20., 20., -20., 20., -20., 20., -20.});
    for (std::size_t i = 0; i < torque.size(); ++i) {
      require(std::isfinite(torque[i]) && std::abs(torque[i]) <= limits[i], "return torque remains bounded");
    }
  }
}

void supporting_stop_interruption()
{
  StateMachine sm(limits);
  reach_rl(sm);
  const Joints q{0., .8, -1.5, 0., 0., .8, -1.5, 0.};
  const Joints previous{1., -2., 3., .2, -1., 2., -3., -.2};
  sm.observe(q, Joints{}, {1., 0., 0., 0.}, {});
  require(sm.request(State::ReturnToSit, q, previous), "supporting return starts");
  sm.update(1.);
  const auto before = sm.torque(q, Joints{});
  require(sm.request(State::EStop, q, before), "right press latches during return");
  require(sm.torque(q, Joints{}) == before, "stop preserves active trajectory and torque");
  sm.update(3.1);
  require(sm.state() == State::EStop, "sit completion cannot clear stop latch");
  require(!sm.request(State::Rl, q), "latched seated stop rejects RL");
  sm.request(State::Damp, q);
  require(sm.torque(q, Joints{}) == Joints{}, "fault cancels static support");
  require(!sm.request(State::TransformUp, q), "fault cannot clear stop latch");
}

void stop_priority_and_loss()
{
  for (bool release_left : {false, true}) {
    JoystickButtons b;
    start_buttons(b);
    b.update(true, true, true, 3.);
    b.update(true, true, false, 4.);
    require(b.update(true, !release_left, true, 5.) == ButtonEvent::Stop, "right press overrides left");
  }
  JoystickButtons b;
  start_buttons(b);
  require(b.update(false, false, false, 3.) == ButtonEvent::Stop, "link/axis loss stops enabled operation");
  require(b.update(true, true, true, 4.) == ButtonEvent::None, "reconnected radio does not resume");
  JoystickButtons startup;
  require(startup.update(false, false, false, 0.) == ButtonEvent::None, "no startup radio does not enable");
  require(startup.update(true, false, true, 1.) == ButtonEvent::None, "radio reconnect held cannot start");
}

void stop_latch_and_damping()
{
  for (State from : {State::Idle, State::TransformUp, State::Sit, State::Rl, State::ReturnToSit, State::Damp}) {
    StateMachine sm(limits);
    if (from == State::Rl || from == State::ReturnToSit) {
      reach_rl(sm);
      if (from == State::ReturnToSit) sm.request(from, kSitPose);
    } else if (from == State::Sit) {
      sm.request(State::TransformUp, kSplayPose);
      sm.update(3.);
    } else {sm.request(from, kSitPose);}
    sm.observe(kSitPose, Joints{}, {1., 0., 0., 0.}, {}, false);
    sm.request(State::Damp, kSitPose);
    require(sm.request(State::EStop, kSitPose), "stop accepted from every phase");
    const Joints velocity{1., -1., 2., -2., 1., -1., 2., -2.};
    const Joints damping{-8., 8., -16., 1., -8., 8., -16., 1.};
    require(sm.torque(kSitPose, velocity) == damping, "software stop retains original damping");
    require(sm.torque(kSitPose, Joints{}) == Joints{}, "stationary stop has zero torque");
    for (State attempt : {State::Idle, State::Damp, State::TransformUp, State::Sit, State::Rl, State::ReturnToSit}) {
      require(!sm.request(attempt, kSitPose), "fault/joystick request cannot clear stop");
      sm.update(100.);
      require(sm.state() == State::EStop, "stop stays latched");
    }
    require(sm.request(State::EStop, kSitPose), "repeated stop is idempotent");
  }
}

int main()
{
  try {
    for (auto test : {decoding, startup_interlock, short_hold_cancels, expected_edges, early_left_press,
      return_trajectory, return_limits, supporting_stop_interruption, stop_priority_and_loss, stop_latch_and_damping}) {
      test();
    }
    std::cout << "PASS: 10 button/state scenarios; startup interlock, one-second hold, short cancellation, RL gate, smooth sit return, limits, immediate stop/loss priority, supporting-stop interruption and fault damping latch\n";
    return 0;
  } catch (const std::exception & e) {
    std::cerr << "FAIL: " << e.what() << '\n';
    return 1;
  }
}
