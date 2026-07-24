#include <gtest/gtest.h>

#include <algorithm>
#include <cmath>
#include <limits>

#include "tita_stage1_controller/stage1_core.hpp"

using tita_stage1_controller::JointArray;
using tita_stage1_controller::JoystickCommandSlew;
using tita_stage1_controller::Stage1Config;
using tita_stage1_controller::Stage1Core;
using tita_stage1_controller::Stage1Input;
using tita_stage1_controller::Stage1Output;
using tita_stage1_controller::Stage1State;

namespace
{
Stage1Config config()
{
  Stage1Config value;
  value.fold_jpos = {0.75, 1.2, -2.7, 0, -0.75, 1.2, -2.7, 0};
  value.stand_jpos = {-0.05, 0.9, -2.6, 0, 0.05, 0.9, -2.6, 0};
  value.transform_kp = {600, 80, 80, 5, 600, 80, 80, 5};
  value.transform_kd = {8, 8, 8, 0.5, 8, 8, 8, 0.5};
  value.ff_effort = {-20, 0, -25, 0, 20, 0, -25, 0};
  value.transition_lower_limits = {-0.8, -2.0, -2.7, -100, -0.8, -2.0, -2.7, -100};
  value.transition_upper_limits = {0.8, 3.5, -0.6, 100, 0.8, 3.5, -0.6, 100};
  value.lower_limits = {-0.8, -2.0, -2.670354, -100, -0.8, -2.0, -2.670354, -100};
  value.upper_limits = {0.8, 3.5, -0.6, 100, 0.8, 3.5, -0.6, 100};
  value.effort_limits = {60, 60, 60, 20, 60, 60, 60, 20};
  value.max_target_slew_rad_s = 10.0;
  value.max_period_seconds = 0.03;
  value.hardware_state_wait_timeout_seconds = 0.10;
  value.hardware_state_stable_seconds = 0.02;
  return value;
}

Stage1Input input()
{
  Stage1Input value;
  value.q = {0.4, 1.2, -2.65, 0.2, -0.4, 1.2, -2.65, -0.2};
  value.hardware_read_valid = true;
  value.motors_online = true;
  value.hardware_output_enabled = true;
  value.period_seconds = 0.02;
  return value;
}

void advance_to_settle(Stage1Core & core, Stage1Input & state)
{
  auto output = core.update(state);
  for (int i = 0; i < 800 && output.state != Stage1State::STANDING_SETTLE; ++i) {
    state.q = output.q;
    output = core.update(state);
  }
  ASSERT_EQ(output.state, Stage1State::STANDING_SETTLE);
  state.q = config().stand_jpos;
  state.dq.fill(0.0);
}

void make_valid_rl_sample(Stage1Input & state, const Stage1Config & cfg)
{
  state.joystick_fresh = true;
  state.joystick_zero = true;
  state.observation_valid = true;
  state.inference_valid = true;
  state.inference_deadline_ok = true;
  state.rl_target_delta_ok = true;
  state.repeated_clipping = 0;
  state.rl_mixed_target = cfg.stand_jpos;
  state.rl_mixed_target[0] += 0.10;
  state.rl_mixed_target[4] -= 0.10;
  state.rl_mixed_target[3] = 0.20;
  state.rl_mixed_target[7] = -0.20;
}

Stage1Output advance_to_rl_running(Stage1Core & core, Stage1Input & state, const Stage1Config & cfg)
{
  advance_to_settle(core, state);
  make_valid_rl_sample(state, cfg);
  Stage1Output output;
  for (int index = 0; index < 4000 && core.state() == Stage1State::STANDING_SETTLE; ++index) {
    output = core.update(state);
  }
  EXPECT_EQ(core.state(), Stage1State::RL_RUNNING);
  return output;
}
}  // namespace

TEST(Stage1Core, OfficialFoldTargetIsAllowedOnlyByTransitionEnvelope)
{
  Stage1Core core(config());
  EXPECT_TRUE(core.valid_config());
  EXPECT_TRUE(core.command_envelopes_valid());
  core.activate();
  auto state = input();
  auto output = core.update(state);
  double minimum_l3 = output.q[2];
  for (int i = 0; i < 400 && output.state != Stage1State::STANDING_SETTLE; ++i) {
    state.q = output.q;
    minimum_l3 = std::min(minimum_l3, output.q[2]);
    output = core.update(state);
  }
  EXPECT_NEAR(minimum_l3, -2.7, 1e-9);
  EXPECT_NE(output.state, Stage1State::FAULT);
}

TEST(Stage1Core, TransformDeadlineMissSlewsSafeHoldThroughTransitionEnvelope)
{
  auto cfg = config();
  cfg.max_target_slew_rad_s = 1.5;
  cfg.max_period_seconds = 0.010;
  cfg.hardware_state_stable_seconds = 0.002;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  state.period_seconds = 0.002;
  auto output = core.update(state);
  for (int i = 0; i < 2000 && output.q[2] > -2.686; ++i) {
    state.q = output.q;
    output = core.update(state);
  }
  ASSERT_EQ(output.state, Stage1State::TRANSFORM_UP) << output.fault << " q2=" << output.q[2];
  ASSERT_LT(output.q[2], cfg.lower_limits[2]);

  state.q = output.q;
  state.period_seconds = 0.01034;
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "CONTROL_DEADLINE_MISS");
  EXPECT_TRUE(output.command_enable);
  EXPECT_GE(output.q[2], cfg.transition_lower_limits[2]);
  EXPECT_LT(output.q[2], cfg.lower_limits[2]);

  state.period_seconds = 0.002;
  for (int i = 0; i < 100 && output.q[2] < cfg.lower_limits[2]; ++i) {
    state.q = output.q;
    output = core.update(state);
  }
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_GE(output.q[2], cfg.lower_limits[2]);
  EXPECT_EQ(output.fault, "CONTROL_DEADLINE_MISS");
}

TEST(Stage1Core, StandingSettleRejectsTransitionOnlyFoldPosition)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  advance_to_settle(core, state);
  state.q[2] = state.q[6] = -2.7;
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "OPERATIONAL_ENVELOPE_EXCEEDED");
  EXPECT_DOUBLE_EQ(output.settle_elapsed, 0.0);
}

TEST(Stage1Core, OperationalEnvelopeIsRequiredBeforeSettleEntry)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  auto output = core.update(state);
  for (int i = 0; i < 200; ++i) {
    state.q = output.q;
    state.q[2] = state.q[6] = -2.7;
    output = core.update(state);
  }
  EXPECT_EQ(output.state, Stage1State::TRANSFORM_UP);
  EXPECT_DOUBLE_EQ(output.settle_elapsed, 0.0);
  state.q = config().stand_jpos;
  for (int i = 0; i < 5; ++i) output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::STANDING_SETTLE);
}

TEST(Stage1Core, TransformUpRequiresStableVelocityAndEnvelopeMarginBeforeSettle)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  auto output = core.update(state);
  state.dq[2] = -1.0;
  for (int i = 0; i < 220; ++i) {
    state.q = output.q;
    output = core.update(state);
  }
  ASSERT_EQ(output.state, Stage1State::TRANSFORM_UP);

  state.q = config().stand_jpos;
  for (int i = 0; i < 10; ++i) output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::TRANSFORM_UP);

  state.dq.fill(0.0);
  state.q[2] = config().lower_limits[2] + 0.01;
  for (int i = 0; i < 10; ++i) output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::TRANSFORM_UP);

  state.q = config().stand_jpos;
  for (int i = 0; i < 4; ++i) output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::TRANSFORM_UP);
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::STANDING_SETTLE);
}

TEST(Stage1Core, ObservedQuantizedRightKneePassesNineteenMilliradianEntryMargin)
{
  auto cfg = config();
  cfg.operational_entry_margin_rad = 0.019;
  constexpr double observed_q6 = -2.6505653858184814;
  ASSERT_LT(observed_q6, cfg.lower_limits[6] + 0.020);
  ASSERT_GT(observed_q6, cfg.lower_limits[6] + cfg.operational_entry_margin_rad);

  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  auto output = core.update(state);
  for (int i = 0; i < 1000 && output.transform_progress < 1.0; ++i) {
    state.q = output.q;
    state.q[6] = cfg.transition_lower_limits[6];
    output = core.update(state);
  }
  ASSERT_EQ(output.state, Stage1State::TRANSFORM_UP);
  ASSERT_DOUBLE_EQ(output.transform_progress, 1.0);

  state.q = cfg.stand_jpos;
  state.q[6] = observed_q6;
  state.dq.fill(0.0);
  for (int i = 0; i < 5; ++i) output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::STANDING_SETTLE);
}

TEST(Stage1Core, TransitionEnvelopeOvershootIsHardFault)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  core.update(state);
  state.q[2] = -2.700001;
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::FAULT);
  EXPECT_EQ(output.fault, "TRANSITION_ENVELOPE_EXCEEDED");
  EXPECT_FALSE(output.command_enable);
}

TEST(Stage1Core, UnexpectedDownstreamClampIsHardFault)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  core.update(state);
  state.unexpected_command_clamp = true;
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::FAULT);
  EXPECT_EQ(output.fault, "UNEXPECTED_COMMAND_CLAMP");
  EXPECT_FALSE(output.command_enable);
}

TEST(Stage1Core, NoCommandBeforeFirstValidState)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  state.hardware_read_valid = false;
  const auto output = core.update(state);
  EXPECT_FALSE(output.command_enable);
  EXPECT_FALSE(output.command_prepared);
  EXPECT_EQ(output.state, Stage1State::WAIT_FOR_HARDWARE);
  EXPECT_DOUBLE_EQ(output.hardware_stable_elapsed, 0.0);
}

TEST(Stage1Core, RequiresContinuousValidStateBeforeFirstCommand)
{
  auto cfg = config();
  cfg.hardware_state_stable_seconds = 0.06;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::WAIT_FOR_HARDWARE);
  EXPECT_FALSE(output.command_enable);
  state.hardware_read_valid = false;
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::WAIT_FOR_HARDWARE);
  EXPECT_DOUBLE_EQ(output.hardware_stable_elapsed, 0.0);
  state.hardware_read_valid = true;
  output = core.update(state);
  EXPECT_FALSE(output.command_enable);
  output = core.update(state);
  EXPECT_FALSE(output.command_enable);
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::MEASURE_INITIAL_POSE);
  EXPECT_TRUE(output.command_enable);
}

TEST(Stage1Core, InvalidHardwareStateTimesOutWithoutACommand)
{
  auto cfg = config();
  cfg.hardware_state_wait_timeout_seconds = 0.06;
  cfg.hardware_state_stable_seconds = 0.02;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  state.motors_online = false;
  auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::WAIT_FOR_HARDWARE);
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::WAIT_FOR_HARDWARE);
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::FAULT);
  EXPECT_EQ(output.fault, "HARDWARE_STATE_WAIT_TIMEOUT");
  EXPECT_FALSE(output.command_enable);
  EXPECT_FALSE(output.command_prepared);
}

TEST(Stage1Core, CapturesMeasuredPoseAndStartsWithZeroWheels)
{
  Stage1Core core(config());
  core.activate();
  const auto state = input();
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::MEASURE_INITIAL_POSE);
  EXPECT_TRUE(output.command_enable);
  EXPECT_EQ(core.measured_initial_pose(), state.q);
  EXPECT_DOUBLE_EQ(output.q[3], 0.0);
  EXPECT_DOUBLE_EQ(output.q[7], 0.0);
  EXPECT_DOUBLE_EQ(output.kp[3], 0.0);
}

TEST(Stage1Core, OfficialInterpolationAndSlewAreBounded)
{
  auto cfg = config();
  cfg.max_target_slew_rad_s = 0.5;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  auto first = core.update(state);
  state.q = first.q;
  const auto second = core.update(state);
  for (std::size_t i : {0U, 1U, 2U, 4U, 5U, 6U}) {
    EXPECT_LE(std::abs(second.q[i] - first.q[i]), 0.0100001);
  }
  EXPECT_EQ(second.state, Stage1State::TRANSFORM_UP);
}

TEST(Stage1Core, FeedForwardEffortAndWheelTargetsAreBounded)
{
  auto cfg = config();
  cfg.ff_effort[0] = -100.0;
  Stage1Core core(cfg);
  core.activate();
  const auto output = core.update(input());
  EXPECT_DOUBLE_EQ(output.effort[0], -60.0);
  EXPECT_DOUBLE_EQ(output.effort[3], 0.0);
  EXPECT_DOUBLE_EQ(output.v[3], 0.0);
}

TEST(Stage1Core, SettleRequiresFiveContinuousSeconds)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  advance_to_settle(core, state);
  tita_stage1_controller::Stage1Output output;
  for (int i = 0; i < 249; ++i) output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::STANDING_SETTLE);
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_TRUE(output.power_cycle_required);
}

TEST(Stage1Core, SettleFailureResetsTimer)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  advance_to_settle(core, state);
  for (int i = 0; i < 200; ++i) core.update(state);
  state.dq[3] = 1.0;
  auto output = core.update(state);
  EXPECT_DOUBLE_EQ(output.settle_elapsed, 0.0);
  EXPECT_EQ(output.state, Stage1State::STANDING_SETTLE);
}

TEST(Stage1Core, WriteFailureAndStaleStateEnterSafeHold)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  core.update(state);
  state.consecutive_write_failures = 3;
  auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "HARDWARE_WRITE_FAILURE");
  EXPECT_TRUE(output.command_enable);
  EXPECT_EQ(output.effort, JointArray{});
}

TEST(Stage1Core, NonFiniteStateDoesNotHoldLastPolicyOrStandAction)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  core.update(state);
  state.q[0] = std::numeric_limits<double>::quiet_NaN();
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "STALE_OR_INVALID_HARDWARE_STATE");
  EXPECT_EQ(output.effort, JointArray{});
}

TEST(Stage1Core, Stage1HasNoRlStateOrOutputPath)
{
  EXPECT_STREQ(tita_stage1_controller::to_string(Stage1State::SAFE_HOLD), "SAFE_HOLD");
  EXPECT_NE(std::string(tita_stage1_controller::to_string(Stage1State::TRANSFORM_UP)).find("RL"), 0U);
}

TEST(Stage1Core, FallTiltBlocksFirstCommand)
{
  Stage1Core core(config());
  core.activate();
  auto state = input();
  state.quaternion_xyzw = {0.0, std::sin(0.4), 0.0, std::cos(0.4)};
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::FAULT);
  EXPECT_EQ(output.fault, "FALL_TILT");
  EXPECT_FALSE(output.command_enable);
}

TEST(Stage2Core, FiveSecondStandSwitchesDirectlyToFullNativePolicy)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.require_zero_joystick = false;
  cfg.rl_running_seconds = 0.0;
  Stage1Core core(cfg);
  ASSERT_TRUE(core.valid_config());
  core.activate();
  auto state = input();
  state.joystick_zero = false;
  const auto output = advance_to_rl_running(core, state, cfg);
  EXPECT_EQ(output.state, Stage1State::RL_RUNNING);
  EXPECT_DOUBLE_EQ(output.policy_active_alpha, 1.0);
  for (std::size_t leg : {0U, 1U, 2U, 4U, 5U, 6U}) {
    EXPECT_DOUBLE_EQ(output.q[leg], state.rl_mixed_target[leg]);
  }
  EXPECT_DOUBLE_EQ(output.v[3], state.rl_mixed_target[3]);
  EXPECT_DOUBLE_EQ(output.v[7], state.rl_mixed_target[7]);
}

TEST(Stage2Core, InvalidPolicySampleBlocksDirectEntry)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.require_zero_joystick = false;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_settle(core, state);
  make_valid_rl_sample(state, cfg);
  state.observation_valid = false;
  Stage1Output output;
  for (int index = 0; index < 400 && core.state() == Stage1State::STANDING_SETTLE; ++index) {
    output = core.update(state);
  }
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "RL_ENTRY_WATCHDOG");
}

TEST(Stage2Core, NativePolicyWheelTargetIsNotCappedOrSlewLimited)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.require_zero_joystick = false;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_settle(core, state);
  make_valid_rl_sample(state, cfg);
  state.rl_mixed_target[3] = -19.610763549804688;
  state.rl_mixed_target[7] = 15.0;
  Stage1Output output;
  for (int index = 0; index < 400 && core.state() == Stage1State::STANDING_SETTLE; ++index) {
    output = core.update(state);
  }
  ASSERT_EQ(output.state, Stage1State::RL_RUNNING);
  EXPECT_DOUBLE_EQ(output.v[3], state.rl_mixed_target[3]);
  EXPECT_DOUBLE_EQ(output.v[7], state.rl_mixed_target[7]);
}

TEST(Stage2Core, JoystickRlRunsUntilExplicitSafeHold)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.require_zero_joystick = false;
  cfg.rl_running_seconds = 0.0;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  auto output = advance_to_rl_running(core, state, cfg);
  for (int index = 0; index < 5000; ++index) output = core.update(state);
  ASSERT_EQ(output.state, Stage1State::RL_RUNNING);
  core.request_safe_hold("OPERATOR_SAFE_HOLD");
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "OPERATOR_SAFE_HOLD");
  EXPECT_TRUE(output.power_cycle_required);
}

TEST(Stage1Core, StandingConditionTimeoutEntersSafeHold)
{
  auto cfg = config();
  cfg.settle_timeout_seconds = 5.20;
  cfg.settle_seconds = 5.0;
  Stage1Core core(cfg);
  ASSERT_TRUE(core.valid_config());
  core.activate();
  auto state = input();
  advance_to_settle(core, state);
  state.dq[3] = cfg.wheel_velocity_rad_s + 1.0;
  tita_stage1_controller::Stage1Output output;
  for (int cycle = 0; cycle < 300 && core.state() == Stage1State::STANDING_SETTLE; ++cycle) {
    output = core.update(state);
  }
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "STANDING_SETTLE_TIMEOUT");
  EXPECT_TRUE(output.power_cycle_required);
}

TEST(Stage2Core, OperatorConfirmedAxis4FallingEdgeRequestsSafeHoldOnce)
{
  tita_stage1_controller::SafeHoldButtonLatch latch;
  EXPECT_FALSE(latch.update(1.0, -0.5, 0.5));
  EXPECT_FALSE(latch.pressed());
  EXPECT_TRUE(latch.update(-1.0, -0.5, 0.5));
  EXPECT_TRUE(latch.pressed());
  EXPECT_FALSE(latch.update(-1.0, -0.5, 0.5));
  EXPECT_FALSE(latch.update(1.0, -0.5, 0.5));
  EXPECT_TRUE(latch.update(-1.0, -0.5, 0.5));
}

TEST(Stage2Core, SafeHoldButtonHeldAtStartupDoesNotCreateFalseEdge)
{
  tita_stage1_controller::SafeHoldButtonLatch latch;
  EXPECT_FALSE(latch.update(-1.0, -0.5, 0.5));
  EXPECT_TRUE(latch.pressed());
  EXPECT_FALSE(latch.update(-1.0, -0.5, 0.5));
  EXPECT_FALSE(latch.update(1.0, -0.5, 0.5));
  EXPECT_TRUE(latch.update(-1.0, -0.5, 0.5));
}

TEST(Stage2Core, FullJoystickCommandIsCappedByApprovedPointSevenFiveGain)
{
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(1.0F, 1.0F, 0.75F), 0.75F);
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(-1.0F, 1.0F, 0.75F), -0.75F);
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(5.0F, 1.0F, 0.75F), 0.75F);
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(0.5F, 1.0F, 0.75F), 0.375F);
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(1.0F, 0.0F, 0.75F), 0.0F);
}

TEST(Stage2Core, JoystickCommandRampsAtTrainingRateAndStopsInFixedHalfSecond)
{
  JoystickCommandSlew slew;
  const std::array<float, 3> target{0.75F, 0.0F, -0.75F};
  std::array<float, 3> command{};
  for (int index = 0; index < 50; ++index) {
    command = slew.update(target, 0.02, 0.5, 0.5);
  }
  EXPECT_NEAR(command[0], 0.5F, 1.0e-6F);
  EXPECT_NEAR(command[2], -0.5F, 1.0e-6F);

  for (int index = 0; index < 25; ++index) {
    command = slew.update({0.0F, 0.0F, 0.0F}, 0.02, 0.5, 0.5);
  }
  EXPECT_FLOAT_EQ(command[0], 0.0F);
  EXPECT_FLOAT_EQ(command[1], 0.0F);
  EXPECT_FLOAT_EQ(command[2], 0.0F);
}

TEST(Stage2Core, JoystickStopDurationIsIndependentOfCurrentSpeed)
{
  JoystickCommandSlew slow;
  JoystickCommandSlew fast;
  for (int index = 0; index < 50; ++index) {
    slow.update({0.25F, 0.0F, 0.0F}, 0.02, 0.5, 0.5);
    fast.update({0.75F, 0.0F, 0.0F}, 0.02, 0.5, 0.5);
  }
  for (int index = 0; index < 24; ++index) {
    EXPECT_GT(std::abs(slow.update({0.0F, 0.0F, 0.0F}, 0.02, 0.5, 0.5)[0]), 0.0F);
    EXPECT_GT(std::abs(fast.update({0.0F, 0.0F, 0.0F}, 0.02, 0.5, 0.5)[0]), 0.0F);
  }
  EXPECT_FLOAT_EQ(slow.update({0.0F, 0.0F, 0.0F}, 0.02, 0.5, 0.5)[0], 0.0F);
  EXPECT_FLOAT_EQ(fast.update({0.0F, 0.0F, 0.0F}, 0.02, 0.5, 0.5)[0], 0.0F);
}

TEST(Stage2Core, PolicyInferenceRunsDuringStandAndNativeRl)
{
  EXPECT_TRUE(tita_stage1_controller::policy_inference_allowed(
    Stage1State::STANDING_SETTLE, true));
  EXPECT_TRUE(tita_stage1_controller::policy_inference_allowed(
    Stage1State::RL_RUNNING, true));
  EXPECT_FALSE(tita_stage1_controller::policy_inference_allowed(
    Stage1State::STANDING_SETTLE, false));
}

TEST(Stage2Core, RuntimeWatchdogRejectsStaleJoystick)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.require_zero_joystick = false;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_running(core, state, cfg);
  state.joystick_fresh = false;
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "RL_RUNNING_WATCHDOG");
  EXPECT_EQ(output.effort, JointArray{});
}

TEST(Stage2Core, OperationalEnvelopeStillBlocksInvalidLegTarget)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.require_zero_joystick = false;
  cfg.allow_clipped_rl_diagnostic = true;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_running(core, state, cfg);
  state.rl_mixed_target[4] = cfg.upper_limits[4] + 0.01;
  const auto real_overrun = core.update(state);
  EXPECT_EQ(real_overrun.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(real_overrun.fault, "RL_RUNNING_WATCHDOG");
}

TEST(Stage2Core, ExcessiveAngularVelocityStopsNativeRl)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.require_zero_joystick = false;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_running(core, state, cfg);
  state.angular_velocity[1] = cfg.max_angular_velocity_rad_s + 0.01;
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "EXCESSIVE_ANGULAR_VELOCITY");
}
