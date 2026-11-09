#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: operator invocation; sources the single workspace.
set -eo pipefail
workspace=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
output=${1:-false}
mode=${2:-teacher}
case $output in false|true) ;; *) echo 'Output must be false or true.' >&2; exit 2;; esac
case $mode in
  teacher) public_launch=sim2real.launch.py ;;
  residual) public_launch=sim2real.residual.torque.launch.py ;;
  *) echo 'Usage: start_sim2real.sh [false|true] [teacher|residual]' >&2; exit 2;;
esac
if [[ -f /opt/ros/humble/setup.bash ]]; then source /opt/ros/humble/setup.bash
else source /opt/ros/jazzy/setup.bash; fi
source "$workspace/install/setup.bash"
export ROS_DOMAIN_ID=42
config_args=()
policy_config=${TITA_POLICY_CONFIG:-$workspace/config/policies.json}
if [[ ! -f $policy_config && -z ${TITA_POLICY_CONFIG:-} ]]; then
    policy_config=$workspace/../config/policies.json
fi
if [[ -f $policy_config ]]; then config_args+=("policy_config:=$policy_config"); fi
exec ros2 launch tita_controller "$public_launch" "output_enabled:=$output" "${config_args[@]}"
