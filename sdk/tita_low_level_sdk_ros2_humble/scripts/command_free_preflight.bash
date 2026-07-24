#!/usr/bin/env bash
set -eo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/humble/setup.bash
source "${repo_root}/direct_ws/install/setup.bash"
source "${repo_root}/lowlevel_ws/install/setup.bash"
set -u

if [[ "$(systemctl is-active tita-bringup.service || true)" != "active" ]]; then
  echo "BLOCKED: vendor service must remain active for command-free preflight" >&2
  exit 1
fi

export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-42}"
export ROS_LOCALHOST_ONLY="${ROS_LOCALHOST_ONLY:-0}"

output="${repo_root}/direct_ws/stage2_preflight.json"
ros2 run tita_low_level_sdk stage2_production_preflight \
  --upstream "${repo_root}/direct_ws/src/ddt_ros2_control" \
  --install "${repo_root}/direct_ws/install" \
  --lowlevel "${repo_root}/lowlevel_ws/src/tita_low_level_sdk" \
  --policy "${TITA_POLICY_PATH:-/home/robot/tita_policy/policy.onnx}" \
  --output "${output}"

python3 - "${output}" <<'PY'
import json
import sys

report = json.load(open(sys.argv[1], encoding="utf-8"))
if not report.get("ready") or report.get("blockers"):
    raise SystemExit("BLOCKED: production preflight did not pass")
if report.get("command_output") != "DISABLED":
    raise SystemExit("BLOCKED: command output was not disabled")
print("COMMAND-FREE PREFLIGHT PASS")
print("COMMAND OUTPUT: DISABLED")
PY
