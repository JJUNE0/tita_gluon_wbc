#include <gtest/gtest.h>

#include <algorithm>
#include <cmath>
#include <limits>

#include "tita_stage1_controller/stage1_core.hpp"

using tita_stage1_controller::JointArray;
using tita_stage1_controller::Stage1Config;
using tita_stage1_controller::Stage1Core;
using tita_stage1_controller::Stage1Input;
using tita_stage1_controller::Stage1State;

namespace
{
Stage1Config config()
{
  Stage1Config value;
  value.fold_jpos = {0.75, 1.2, -2.7, 0, -0.75, 1.2, -2.7, 0};
  value.stand_jpos = {-0.05, 0.9, -2.6, 0, 0.05, 0.9, -2.6, 0};
  value.policy_stand_jpos = {0.1, 0.8, -1.5, 0, 0.1, 0.8, -1.5, 0};
  value.transform_kp = {600, 80, 80, 5, 600, 80, 80, 5};
  value.transform_kd = {8, 8, 8, 0.5, 8, 8, 8, 0.5};
  value.ff_effort = {-20, 0, -25, 0, 20, 0, -25, 0};
  value.transition_lower_limits = {-0.8, -2.0, -2.7, -100, -0.8, -2.0, -2.7, -100};
  value.transition_upper_limits = {0.8, 3.5, -0.6, 100, 0.8, 3.5, -0.6, 100};
  value.lower_limits = {-0.8, -2.0, -2.670354, -100, -0.8, -2.0, -2.670354, -100};
  value.upper_limits = {0.8, 3.5, -0.6, 100, 0.8, 3.5, -0.6, 100};
  value.effort_limits = {60, 60, 60, 20, 60, 60, 60, 20};
  value.max_target_slew_rad_s = 10.0;
  value.handoff_seconds = 0.20;
  value.handoff_settle_seconds = 0.10;
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
  state.history_complete = true;
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

void advance_to_rl_prepare(Stage1Core & core, Stage1Input & state, const Stage1Config & cfg)
{
  advance_to_settle(core, state);
  make_valid_rl_sample(state, cfg);
  for (int index = 0; index < 251; ++index) {
    const auto output = core.update(state);
    state.q = output.q;
  }
  ASSERT_EQ(core.state(), Stage1State::RL_BLEND);
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

TEST(Stage2Core, IncompleteHistoryAndNonzeroJoyBlockBlend)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);
  state.history_complete = false;
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "RL_BLEND_WATCHDOG");
}

TEST(Stage2Core, JoystickRlUsesSamePipelineAndAllowsFreshNonzeroCommand)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.require_zero_joystick = false;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);
  state.joystick_zero = false;
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::RL_BLEND);
  EXPECT_TRUE(output.command_enable);
}

TEST(Stage2Core, OfficialStandFeedsDirectlyIntoPrepareWithoutPolicyStandHold)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_settle(core, state);
  make_valid_rl_sample(state, cfg);
  for (int index = 0; index < 251; ++index) core.update(state);
  auto output = core.update(state);
  EXPECT_EQ(core.state(), Stage1State::RL_BLEND);
  EXPECT_LE(std::abs(output.q[0] - cfg.stand_jpos[0]), 0.0040001);
  EXPECT_LE(std::abs(output.q[2] - cfg.stand_jpos[2]), 0.0040001);
}

TEST(Stage2Core, StablePrepareRunsBoundedMonotonicBlendThenTimedSafeHold)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.rl_running_seconds = 1.0;
  cfg.max_leg_target_slew_rad_s = 0.5;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);
  tita_stage1_controller::Stage1Output output;
  double previous_alpha = 0.0;
  JointArray previous_q = cfg.stand_jpos;
  for (int index = 0; index < 50; ++index) {
    output = core.update(state);
    EXPECT_GE(output.rl_blend_alpha, previous_alpha);
    EXPECT_LE(output.rl_blend_alpha, 1.0);
    for (std::size_t leg : {0U, 1U, 2U, 4U, 5U, 6U}) {
      EXPECT_LE(std::abs(output.q[leg] - previous_q[leg]), 0.0100001);
    }
    previous_alpha = output.rl_blend_alpha;
    previous_q = output.q;
  }
  ASSERT_EQ(core.state(), Stage1State::RL_RUNNING);
  EXPECT_NEAR(output.rl_blend_alpha, 1.0, 1e-12);
  for (int index = 0; index < 48; ++index) output = core.update(state);
  EXPECT_EQ(core.state(), Stage1State::RL_RUNNING);
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_TRUE(output.power_cycle_required);
  EXPECT_EQ(output.effort, JointArray{});
}

TEST(Stage2Core, UnlimitedJoystickRlRequiresExplicitSafeHold)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.require_zero_joystick = false;
  cfg.rl_running_seconds = 0.0;
  Stage1Core core(cfg);
  ASSERT_TRUE(core.valid_config());
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);
  tita_stage1_controller::Stage1Output output;
  while (core.state() == Stage1State::RL_BLEND) output = core.update(state);
  ASSERT_EQ(core.state(), Stage1State::RL_RUNNING);
  for (int index = 0; index < 5000; ++index) output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::RL_RUNNING);
  core.request_safe_hold("OPERATOR_SAFE_HOLD");
  output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "OPERATOR_SAFE_HOLD");
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

TEST(Stage2Core, FullJoystickCommandIsCappedByApprovedPointThreeGain)
{
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(1.0F, 1.0F, 0.3F), 0.3F);
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(-1.0F, 1.0F, 0.3F), -0.3F);
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(5.0F, 1.0F, 0.3F), 0.3F);
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(0.5F, 1.0F, 0.3F), 0.15F);
  EXPECT_FLOAT_EQ(tita_stage1_controller::bounded_joy_command(1.0F, 0.0F, 0.3F), 0.0F);
}

TEST(Stage2Core, OnePolicyPeriodBlendIsTenBoundedControllerCycles)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.rl_blend_seconds = 0.02;
  cfg.max_leg_target_slew_rad_s = 3000.0;
  cfg.max_wheel_accel_rad_s = 15000.0;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_settle(core, state);
  make_valid_rl_sample(state, cfg);
  state.period_seconds = 0.002;
  for (int cycle = 0; cycle < 2501 && core.state() != Stage1State::RL_BLEND; ++cycle) {
    const auto settle_output = core.update(state);
    state.q = settle_output.q;
  }
  ASSERT_EQ(core.state(), Stage1State::RL_BLEND);
  double previous_alpha = 0.0;
  tita_stage1_controller::Stage1Output output;
  for (int cycle = 1; cycle <= 10; ++cycle) {
    output = core.update(state);
    EXPECT_GE(output.rl_blend_alpha, previous_alpha);
    EXPECT_NEAR(output.rl_blend_alpha, 0.1 * cycle, 1.0e-9);
    previous_alpha = output.rl_blend_alpha;
  }
  EXPECT_EQ(output.state, Stage1State::RL_RUNNING);
  EXPECT_NEAR(output.rl_blend_alpha, 1.0, 1.0e-12);
}

TEST(Stage2Core, PolicyTargetIsFrozenDuringBoundedBlend)
{
  EXPECT_TRUE(tita_stage1_controller::policy_inference_allowed(
    Stage1State::STANDING_SETTLE, true));
  EXPECT_TRUE(tita_stage1_controller::policy_inference_allowed(
    Stage1State::RL_RUNNING, true));
  EXPECT_FALSE(tita_stage1_controller::policy_inference_allowed(
    Stage1State::RL_BLEND, true));
  EXPECT_FALSE(tita_stage1_controller::policy_inference_allowed(
    Stage1State::STANDING_SETTLE, false));
}

TEST(Stage2Core, BlendFaultRejectsLastRlActionAndEntersSafeHold)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);
  state.joystick_fresh = false;
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "RL_BLEND_WATCHDOG");
  EXPECT_DOUBLE_EQ(output.v[3], 0.0);
  EXPECT_DOUBLE_EQ(output.v[7], 0.0);
  EXPECT_EQ(output.effort, JointArray{});
}

TEST(Stage2Core, RepeatedClippingAndOperationalEnvelopeBlockRl)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);
  state.repeated_clipping = cfg.max_repeated_clipping + 1;
  const auto clipping_output = core.update(state);
  EXPECT_EQ(clipping_output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(clipping_output.fault, "RL_BLEND_WATCHDOG");
}

TEST(Stage2Core, ClippedDiagnosticContinuesBoundedBlendButKeepsOtherWatchdogs)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.allow_clipped_rl_diagnostic = true;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);
  state.rl_target_delta_ok = false;
  state.repeated_clipping = cfg.max_repeated_clipping + 100;
  const auto clipped = core.update(state);
  EXPECT_EQ(clipped.state, Stage1State::RL_BLEND);
  EXPECT_GT(clipped.rl_blend_alpha, 0.0);
  state.joystick_fresh = false;
  const auto stale = core.update(state);
  EXPECT_EQ(stale.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(stale.fault, "RL_BLEND_WATCHDOG");
}

TEST(Stage2Core, OperationalToleranceCoversFloatBoundaryButNotRealOverrun)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.allow_clipped_rl_diagnostic = true;
  cfg.operational_envelope_tolerance_rad = 1.0e-6;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);

  state.rl_mixed_target[4] = cfg.upper_limits[4] + 0.5e-6;
  const auto rounding_only = core.update(state);
  EXPECT_EQ(rounding_only.state, Stage1State::RL_BLEND);

  state.rl_mixed_target[4] = cfg.upper_limits[4] + 2.0e-6;
  const auto real_overrun = core.update(state);
  EXPECT_EQ(real_overrun.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(real_overrun.fault, "RL_BLEND_WATCHDOG");
}

TEST(Stage2Core, ExcessiveAngularVelocityStopsBlendBeforeFallTilt)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);
  state.angular_velocity[1] = cfg.max_angular_velocity_rad_s + 0.01;
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "EXCESSIVE_ANGULAR_VELOCITY");
}

TEST(Stage2Core, ApprovedAngularVelocityMarginStillFailsClosedAboveBoundary)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.max_angular_velocity_rad_s = 2.5;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);

  state.angular_velocity = {0.0, 2.49, 0.0};
  EXPECT_EQ(core.update(state).state, Stage1State::RL_BLEND);

  state.angular_velocity = {0.0, 2.51, 0.0};
  const auto output = core.update(state);
  EXPECT_EQ(output.state, Stage1State::SAFE_HOLD);
  EXPECT_EQ(output.fault, "EXCESSIVE_ANGULAR_VELOCITY");
}

TEST(Stage2Core, SimMatchedBoundsApplyFullCandidateWithinOneRealControlCycle)
{
  auto cfg = config();
  cfg.stage2_enabled = true;
  cfg.max_leg_target_slew_rad_s = 3000.0;
  cfg.max_wheel_velocity_rad_s = 15.0;
  cfg.max_wheel_accel_rad_s = 15000.0;
  Stage1Core core(cfg);
  core.activate();
  auto state = input();
  advance_to_rl_prepare(core, state, cfg);
  for (int index = 0; index < 50; ++index) core.update(state);
  ASSERT_EQ(core.state(), Stage1State::RL_RUNNING);

  state.period_seconds = 0.002;
  state.rl_mixed_target = cfg.stand_jpos;
  state.rl_mixed_target[0] = cfg.lower_limits[0];
  state.rl_mixed_target[1] = cfg.upper_limits[1];
  state.rl_mixed_target[2] = cfg.upper_limits[2];
  state.rl_mixed_target[3] = -15.0;
  state.rl_mixed_target[4] = cfg.upper_limits[4];
  state.rl_mixed_target[5] = cfg.lower_limits[5];
  state.rl_mixed_target[6] = cfg.lower_limits[6];
  state.rl_mixed_target[7] = 15.0;
  const auto output = core.update(state);
  for (std::size_t leg : {0U, 1U, 2U, 4U, 5U, 6U}) {
    EXPECT_NEAR(output.q[leg], state.rl_mixed_target[leg], 1e-12);
  }
  EXPECT_NEAR(output.v[3], -15.0, 1e-12);
  EXPECT_NEAR(output.v[7], 15.0, 1e-12);
}
