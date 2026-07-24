#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
expected_start="0a2bca4a146f9127ad558b50ca745826cc93ee920f3bb9538521555ea94f97b3"
expected_policy="d53a5b0b69e5382dc5f40909ecaa7481221397aa3b3400c922b13a33576273e6"

start_path="${repo_root}/direct_ws/src/ddt_ros2_control/start.bash"
actual_start="$(sha256sum "${start_path}" | awk '{print $1}')"
[[ "${actual_start}" == "${expected_start}" ]] || {
  echo "start.bash SHA256 mismatch" >&2
  exit 1
}
echo "start.bash SHA256 PASS: ${actual_start}"

policy_path="${TITA_POLICY_PATH:-/home/robot/tita_policy/policy.onnx}"
if [[ -f "${policy_path}" ]]; then
  actual_policy="$(sha256sum "${policy_path}" | awk '{print $1}')"
  [[ "${actual_policy}" == "${expected_policy}" ]] || {
    echo "policy SHA256 mismatch" >&2
    exit 1
  }
  echo "policy SHA256 PASS: ${actual_policy}"
else
  echo "policy not present; expected SHA256: ${expected_policy}"
fi

