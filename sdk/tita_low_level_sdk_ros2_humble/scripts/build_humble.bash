#!/usr/bin/env bash
set -eo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/humble/setup.bash
set -u

if [[ ! -d "${repo_root}/direct_ws/src/ddt_ros2_control/.git" ]]; then
  echo "Run scripts/bootstrap_upstream.bash first." >&2
  exit 1
fi

cd "${repo_root}/direct_ws"
colcon build --packages-select \
  ros_utils tita_robot teleop_command tita_description hardware_bridge tita_stage1_controller
set +u
source install/setup.bash
set -u
colcon test --packages-select hardware_bridge tita_stage1_controller
colcon test-result --test-result-base build/hardware_bridge --verbose
colcon test-result --test-result-base build/tita_stage1_controller --verbose

cd "${repo_root}/lowlevel_ws"
colcon build --packages-select tita_low_level_sdk
set +u
source install/setup.bash
set -u
colcon test --packages-select tita_low_level_sdk
colcon test-result --test-result-base build/tita_low_level_sdk --verbose

echo "ROS 2 Humble source build and package tests completed."
