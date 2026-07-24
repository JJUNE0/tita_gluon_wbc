#include <gtest/gtest.h>

#include <cmath>
#include <limits>

#include "tita_stage1_controller/rl_pipeline.hpp"

using tita_stage1_controller::ActionAdapter;
using tita_stage1_controller::FloatJointArray;
using tita_stage1_controller::ObservationBuilder;
using tita_stage1_controller::ObservationInput;
using tita_stage1_controller::ObservationArray;
using tita_stage1_controller::OnnxPolicyRunner;

TEST(RlObservation, BlendPreviousActionTracksAppliedRlContribution)
{
  const FloatJointArray raw = {1, -2, 3, -4, 5, -6, 7, -8};
  const auto zero = tita_stage1_controller::applied_policy_action_feedback(raw, 0.0F);
  const auto quarter = tita_stage1_controller::applied_policy_action_feedback(raw, 0.25F);
  const auto full = tita_stage1_controller::applied_policy_action_feedback(raw, 1.0F);
  EXPECT_EQ(zero, FloatJointArray{});
  EXPECT_EQ(full, raw);
  for (std::size_t index = 0; index < raw.size(); ++index) {
    EXPECT_FLOAT_EQ(quarter[index], 0.25F * raw[index]);
  }
}

TEST(RlObservation, ExactPythonFieldOrderScaleAndProjectedGravity)
{
  ObservationInput input;
  input.joint_position_native = {0.2F, 1.0F, -1.8F, 123.0F, -0.1F, 0.7F, -1.4F, -456.0F};
  input.joint_velocity_native = {1, 2, 3, 4, 5, 6, 7, 8};
  input.angular_velocity = {0.4F, -0.8F, 1.2F};
  input.command_vx_vy_yaw = {0.1F, -0.2F, 0.4F};
  input.previous_action_policy_order = {0, 1, 2, 3, 4, 5, 6, 7};
  const auto result = ObservationBuilder{}.build(input);
  ASSERT_TRUE(result.finite);
  EXPECT_FLOAT_EQ(result.values[0], 0.1F);
  EXPECT_FLOAT_EQ(result.values[1], -0.2F);
  EXPECT_FLOAT_EQ(result.values[2], 0.3F);
  EXPECT_FLOAT_EQ(result.values[3], 0.0F);
  EXPECT_FLOAT_EQ(result.values[4], 0.0F);
  EXPECT_FLOAT_EQ(result.values[5], -1.0F);
  EXPECT_FLOAT_EQ(result.values[6], 0.2F);
  EXPECT_FLOAT_EQ(result.values[7], -0.4F);
  EXPECT_FLOAT_EQ(result.values[8], 0.1F);
  // policy order [L1,R1,L2,R2,L3,R3,L4,R4], wheel positions zeroed first.
  const std::array<float, 8> expected_position =
    {0.1F, -0.2F, 0.2F, -0.1F, -0.3F, 0.1F, 0.0F, 0.0F};
  for (std::size_t index = 0; index < 8; ++index) {
    EXPECT_NEAR(result.values[9 + index], expected_position[index], 1.0e-6F);
  }
  const std::array<float, 8> expected_velocity =
    {0.05F, 0.25F, 0.10F, 0.30F, 0.15F, 0.35F, 0.20F, 0.40F};
  for (std::size_t index = 0; index < 8; ++index) {
    EXPECT_NEAR(result.values[17 + index], expected_velocity[index], 1.0e-6F);
    EXPECT_FLOAT_EQ(result.values[25 + index], static_cast<float>(index));
  }
}

TEST(RlObservation, QuaternionAndNonFiniteValidationMatchPython)
{
  ObservationInput input;
  input.quaternion_xyzw = {0.0F, std::sin(0.25F), 0.0F, std::cos(0.25F)};
  const auto result = ObservationBuilder{}.build(input);
  ASSERT_TRUE(result.finite);
  EXPECT_NEAR(result.projected_gravity[0], std::sin(0.5F), 1.0e-6F);
  EXPECT_NEAR(result.projected_gravity[2], -std::cos(0.5F), 1.0e-6F);
  input.joint_velocity_native[2] = std::numeric_limits<float>::quiet_NaN();
  EXPECT_FALSE(ObservationBuilder{}.build(input).finite);
}

TEST(RlAction, NativePolicyOutputAndMixedSemanticsMatchValidatedSim2sim)
{
  const FloatJointArray policy = {1, 2, 3, 4, 5, 6, 7, 8};
  const auto result = ActionAdapter{}.compute(policy);
  ASSERT_TRUE(result.finite);
  EXPECT_EQ(result.action_native_order, policy);
  // Exact policy targets are retained even when the explicit safety candidate is clipped.
  EXPECT_FLOAT_EQ(result.rl_target_native[0], 0.35F);
  EXPECT_FLOAT_EQ(result.rl_target_native[1], 1.30F);
  EXPECT_FLOAT_EQ(result.rl_target_native[2], -0.75F);
  EXPECT_FLOAT_EQ(result.rl_target_native[3], 20.0F);
  EXPECT_FLOAT_EQ(result.rl_target_native[7], 40.0F);
  EXPECT_FLOAT_EQ(result.limited_target_native[0], 0.35F);
  EXPECT_FLOAT_EQ(result.limited_target_native[1], 1.05F);
  EXPECT_FLOAT_EQ(result.limited_target_native[2], -1.25F);
  EXPECT_FLOAT_EQ(result.limited_target_native[3], 5.0F);
  EXPECT_FLOAT_EQ(result.limited_target_native[7], 5.0F);
  EXPECT_TRUE(result.clipping_mask[1]);
  EXPECT_TRUE(result.clipping_mask[3]);
}

TEST(RlAction, PreservedControlledIsaacTraceUsesNativeWheelIndices)
{
  const FloatJointArray policy = {
    -1.0296727F, -0.17814201F, 0.13371354F, 0.41985422F,
    0.21155298F, -0.07268497F, -0.51115394F, 0.21017869F};
  const auto result = ActionAdapter{}.compute(policy, 100.0F, 100.0F);
  ASSERT_TRUE(result.finite);
  EXPECT_EQ(result.action_native_order, policy);
  EXPECT_NEAR(result.rl_target_native[0], -0.15741819F, 1.0e-6F);
  EXPECT_NEAR(result.rl_target_native[1], 0.75546450F, 1.0e-6F);
  EXPECT_NEAR(result.rl_target_native[2], -1.4665716F, 1.0e-6F);
  EXPECT_NEAR(result.rl_target_native[3], 2.0992711F, 1.0e-6F);
  EXPECT_NEAR(result.rl_target_native[4], 0.15288824F, 1.0e-6F);
  EXPECT_NEAR(result.rl_target_native[5], 0.78182876F, 1.0e-6F);
  EXPECT_NEAR(result.rl_target_native[6], -1.6277885F, 1.0e-6F);
  EXPECT_NEAR(result.rl_target_native[7], 1.0508934F, 1.0e-6F);
}

TEST(RlAction, NativePolicyPathMatchesMujocoWithoutTargetClipping)
{
  const FloatJointArray policy = {
    -0.98586655F, 0.03663523F, -0.44292769F, -3.9221527F,
    0.44705975F, 0.11435896F, 0.59563988F, 3.0868164F};
  const auto result = ActionAdapter{}.compute_native_policy(policy);
  ASSERT_TRUE(result.finite);
  EXPECT_EQ(result.clipping_count, 0U);
  EXPECT_FLOAT_EQ(result.limited_target_native[0], 0.1F + 0.25F * policy[0]);
  EXPECT_FLOAT_EQ(result.limited_target_native[3], 5.0F * policy[3]);
  EXPECT_FLOAT_EQ(result.limited_target_native[7], 5.0F * policy[7]);
  EXPECT_LT(result.limited_target_native[3], -19.0F);
  EXPECT_GT(result.limited_target_native[7], 15.0F);
}

TEST(RlAction, OperationalEnvelopeClampIsExplicitInTargetAndMask)
{
  FloatJointArray policy{};
  // Policy output index 4 is native R1: 0.1 + 3.2 * 0.25 = 0.9 rad.
  policy[4] = 3.2F;
  ActionAdapter adapter;
  auto result = adapter.compute(policy, 1.0F, 15.0F);
  ASSERT_TRUE(result.finite);
  ASSERT_FALSE(result.clipping_mask[4]);

  FloatJointArray lower{};
  FloatJointArray upper{};
  lower.fill(-100.0F);
  upper.fill(100.0F);
  upper[4] = 0.785398F;
  result = adapter.apply_operational_envelope(result, lower, upper);

  ASSERT_TRUE(result.finite);
  EXPECT_FLOAT_EQ(result.rl_target_native[4], 0.9F);
  EXPECT_FLOAT_EQ(result.limited_target_native[4], 0.785398F);
  EXPECT_TRUE(result.clipping_mask[4]);
  EXPECT_EQ(result.clipping_count, 1U);
}

#ifdef TITA_TEST_POLICY_PATH
TEST(RlOnnx, FixedInterfaceHashAndOutputParity)
{
  OnnxPolicyRunner runner;
  const auto status = runner.load(
    TITA_TEST_POLICY_PATH,
    "025ad9b5a2022a9b2854623a3ff7149a73b3118585eb3744a1c5ab5e3e90090c");
  ASSERT_TRUE(status.loaded) << status.detail;
  EXPECT_EQ(status.input_names[0], "nn_input0");
  EXPECT_TRUE(status.input_names[1].empty());
  EXPECT_EQ(status.output_name, "nn_output");
  ObservationArray observation{};
  FloatJointArray action{};
  double inference_ms = 0.0;
  std::string error;
  ASSERT_TRUE(runner.infer(observation, action, inference_ms, error)) << error;
  const FloatJointArray expected = {
    0.118399784F, -0.109461874F, -0.353689641F, -1.3064698F,
    -0.189832374F, -0.0797345191F, -0.167744935F, -0.887791455F};
  for (std::size_t index = 0; index < action.size(); ++index) {
    EXPECT_NEAR(action[index], expected[index], 2.0e-5F);
  }
  EXPECT_GT(inference_ms, 0.0);
}

TEST(RlOnnx, HashMismatchAndNonFiniteInputFailClosed)
{
  OnnxPolicyRunner runner;
  EXPECT_FALSE(runner.load(TITA_TEST_POLICY_PATH, std::string(64, '0')).loaded);
  const auto status = runner.load(
    TITA_TEST_POLICY_PATH,
    "025ad9b5a2022a9b2854623a3ff7149a73b3118585eb3744a1c5ab5e3e90090c");
  ASSERT_TRUE(status.loaded);
  ObservationArray observation{};
  observation[0] = std::numeric_limits<float>::infinity();
  FloatJointArray action{};
  double inference_ms = 0.0;
  std::string error;
  EXPECT_FALSE(runner.infer(observation, action, inference_ms, error));
}

#ifdef TITA_TEST_DIAGNOSTIC_POLICY_PATH
TEST(RlOnnx, EstimatorDiagnosticOutputIsFiniteAndRequired)
{
  OnnxPolicyRunner runner;
  const auto status = runner.load(
    TITA_TEST_DIAGNOSTIC_POLICY_PATH,
    "6bcd8c4028507dc636f58eee64ad9cfb9c7cc2d948889df4217ba91ba9e8a121", true);
  ASSERT_TRUE(status.loaded) << status.detail;
  EXPECT_TRUE(status.estimator_output_available);
  ObservationArray observation{};
  FloatJointArray action{};
  tita_stage1_controller::EstimatorArray estimator{};
  double inference_ms = 0.0;
  std::string error;
  ASSERT_TRUE(runner.infer(observation, action, estimator, inference_ms, error)) << error;
  for (const float value : estimator) EXPECT_TRUE(std::isfinite(value));
}
#endif
#endif
