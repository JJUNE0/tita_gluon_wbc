// Copyright 2026 TITA operator
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <gtest/gtest.h>

#include <algorithm>

#include "hardware_interface/system_interface.hpp"
#include "hardware_bridge/hardware_bridge_node.hpp"
#include "pluginlib/class_loader.hpp"

TEST(HardwareBridgePlugin, LoadsWithoutOpeningHardware)
{
  pluginlib::ClassLoader<hardware_interface::SystemInterface> loader(
    "hardware_interface", "hardware_interface::SystemInterface");
  const auto declared = loader.getDeclaredClasses();
  EXPECT_NE(std::find(declared.begin(), declared.end(),
    "tita_locomotion::HardwareBridge"), declared.end());
  auto bridge = loader.createSharedInstance("tita_locomotion::HardwareBridge");
  ASSERT_NE(bridge, nullptr);
}

TEST(HardwareBridgeMotorStatus, DistinguishesUnavailableCompleteAndPartialStatus)
{
  const auto unavailable = tita_locomotion::summarize_motor_status(
    std::vector<uint16_t>(8U, 0U), 8U);
  EXPECT_FALSE(unavailable.available);
  EXPECT_FALSE(unavailable.all_online);
  EXPECT_TRUE(unavailable.consistent);

  const auto complete = tita_locomotion::summarize_motor_status(
    std::vector<uint16_t>(8U, 1U), 8U);
  EXPECT_TRUE(complete.available);
  EXPECT_TRUE(complete.all_online);
  EXPECT_TRUE(complete.consistent);

  auto partial_values = std::vector<uint16_t>(8U, 1U);
  partial_values[3] = 0U;
  const auto partial = tita_locomotion::summarize_motor_status(partial_values, 8U);
  EXPECT_TRUE(partial.available);
  EXPECT_FALSE(partial.all_online);
  EXPECT_FALSE(partial.consistent);

  const auto malformed = tita_locomotion::summarize_motor_status(
    std::vector<uint16_t>(7U, 1U), 8U);
  EXPECT_FALSE(malformed.consistent);
}
