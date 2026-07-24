#include <gtest/gtest.h>

#include <algorithm>
#include <memory>
#include <set>
#include <vector>

#include "controller_interface/controller_interface.hpp"
#include "pluginlib/class_loader.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp/version.h"

namespace
{
const std::vector<std::string> kJoints = {
  "joint_left_leg_1", "joint_left_leg_2", "joint_left_leg_3", "joint_left_leg_4",
  "joint_right_leg_1", "joint_right_leg_2", "joint_right_leg_3", "joint_right_leg_4"};

std::shared_ptr<controller_interface::ControllerInterface> make_controller(
  pluginlib::ClassLoader<controller_interface::ControllerInterface> & loader,
  const std::string & name, const bool stage2 = false)
{
  auto controller = loader.createSharedInstance("tita_stage1_controller/Stage1Controller");
  rclcpp::NodeOptions options;
  std::vector<rclcpp::Parameter> parameters = {
    rclcpp::Parameter("joints", kJoints), rclcpp::Parameter("stage1_only", !stage2),
    rclcpp::Parameter("stage2.enabled", stage2)};
#ifdef TITA_TEST_POLICY_PATH
  if (stage2) {
    parameters.emplace_back("stage2.policy_path", TITA_TEST_POLICY_PATH);
    parameters.emplace_back(
      "stage2.policy_sha256",
      "d53a5b0b69e5382dc5f40909ecaa7481221397aa3b3400c922b13a33576273e6");
  }
#endif
  options.parameter_overrides(parameters);
#if RCLCPP_VERSION_MAJOR >= 21
  EXPECT_EQ(
    controller->init(name, "", 500U, "", options), controller_interface::return_type::OK);
#else
  EXPECT_EQ(controller->init(name, "", options), controller_interface::return_type::OK);
#endif
  return controller;
}
}  // namespace

#ifdef TITA_TEST_POLICY_PATH
TEST(Stage1ControllerPlugin, LoadsStage2ModeAndPolicyBeforeHardwareActivation)
{
  if (!rclcpp::ok()) rclcpp::init(0, nullptr);
  pluginlib::ClassLoader<controller_interface::ControllerInterface> loader(
    "controller_interface", "controller_interface::ControllerInterface");
  const auto controller = make_controller(loader, "stage2_policy_load", true);
  ASSERT_NE(controller, nullptr);
}
#endif

TEST(Stage1ControllerPlugin, LoadsProductionController)
{
  if (!rclcpp::ok()) rclcpp::init(0, nullptr);
  pluginlib::ClassLoader<controller_interface::ControllerInterface> loader(
    "controller_interface", "controller_interface::ControllerInterface");
  const auto declared = loader.getDeclaredClasses();
  EXPECT_NE(
    std::find(declared.begin(), declared.end(),
      "tita_stage1_controller/Stage1Controller"), declared.end());
  auto controller = loader.createSharedInstance("tita_stage1_controller/Stage1Controller");
  ASSERT_NE(controller, nullptr);
}

TEST(Stage1ControllerPlugin, ClaimsExactlyOneUniqueEightJointCommandSet)
{
  if (!rclcpp::ok()) rclcpp::init(0, nullptr);
  pluginlib::ClassLoader<controller_interface::ControllerInterface> loader(
    "controller_interface", "controller_interface::ControllerInterface");
  const auto controller = make_controller(loader, "stage1_claim_a");
  const auto command = controller->command_interface_configuration();
  ASSERT_EQ(command.type, controller_interface::interface_configuration_type::INDIVIDUAL);
  ASSERT_EQ(command.names.size(), 164U);  // 46 control + 118 fixed-shape Stage 2 metadata.
  const std::set<std::string> unique(command.names.begin(), command.names.end());
  EXPECT_EQ(unique.size(), command.names.size());
  for (const auto & joint : kJoints) {
    for (const auto & interface : {"position", "velocity", "effort", "kp", "kd"}) {
      EXPECT_EQ(unique.count(joint + "/" + interface), 1U);
    }
  }
  EXPECT_EQ(unique.count("hardware_bridge/command_enable"), 1U);
  for (const auto & interface : {
      "stage1_state", "controller_sequence", "transform_progress", "settle_elapsed",
      "command_prepared"}) {
    EXPECT_EQ(unique.count(std::string("hardware_bridge/") + interface), 1U);
  }
  for (const auto & interface : {
      "rl_prepare_elapsed", "rl_blend_alpha", "rl_running_elapsed", "history_valid_count",
      "inference_ms", "joy_fresh", "joy_zero", "repeated_clipping", "logger_flush_request"})
  {
    EXPECT_EQ(unique.count(std::string("hardware_bridge/") + interface), 1U);
  }
  for (const auto & interface : {
      "joy_age_ms", "joy_command_vx", "joy_command_vy", "joy_command_yaw"})
  {
    EXPECT_EQ(unique.count(std::string("hardware_bridge/") + interface), 1U);
  }
  for (std::size_t i = 0; i < 33; ++i) {
    EXPECT_EQ(unique.count("hardware_bridge/obs_current" + std::to_string(i)), 1U);
  }
  for (const auto & prefix : {
      "limited_target", "blended_target", "clipping_mask", "joy_axis"})
  {
    for (std::size_t i = 0; i < 8; ++i) {
      EXPECT_EQ(unique.count(std::string("hardware_bridge/") + prefix + std::to_string(i)), 1U);
    }
  }

  const auto state = controller->state_interface_configuration();
  EXPECT_EQ(state.type, controller_interface::interface_configuration_type::INDIVIDUAL);
  EXPECT_EQ(state.names.size(), 57U);  // 24 joint + 10 IMU + 15 status + 8 correlation.
  const std::set<std::string> unique_state(state.names.begin(), state.names.end());
  for (const auto & interface : {
      "imu_fresh", "motors_fresh", "joint_vectors_valid", "state_values_finite",
      "motor_status_all_online", "motor_status_available"}) {
    EXPECT_EQ(unique_state.count(std::string("hardware_bridge/") + interface), 1U);
  }
  EXPECT_EQ(unique_state.count("hardware_bridge/logger_flushed_sequence"), 1U);
  for (std::size_t i = 0; i < 8; ++i) {
    EXPECT_EQ(unique_state.count("hardware_bridge/last_command_q" + std::to_string(i)), 1U);
  }
}

TEST(Stage1ControllerPlugin, DuplicateInstanceRequestsIdenticalExclusiveInterfaces)
{
  if (!rclcpp::ok()) rclcpp::init(0, nullptr);
  pluginlib::ClassLoader<controller_interface::ControllerInterface> loader(
    "controller_interface", "controller_interface::ControllerInterface");
  const auto first = make_controller(loader, "stage1_claim_first");
  const auto second = make_controller(loader, "stage1_claim_second");
  const auto first_names = first->command_interface_configuration().names;
  const auto second_names = second->command_interface_configuration().names;
  EXPECT_EQ(first_names, second_names);
  EXPECT_FALSE(first_names.empty());
  // controller_manager treats INDIVIDUAL command interfaces as exclusive resources, so a second
  // active instance necessarily conflicts on all of these names rather than creating a writer.
}
