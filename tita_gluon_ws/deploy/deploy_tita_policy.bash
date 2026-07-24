#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
POLICY="${1:-${ROOT}/deploy/tita/policy.onnx}"
ROBOT="${TITA_SSH:-robot@192.168.0.28}"
STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP="${ROOT}/tita_backup/policies/${STAMP}"

CONTROLLER="${ROOT}/direct_ws/src/tita_stage1_controller"
LOWLEVEL="${ROOT}/tita_low_level_sdk"
CONFIG="${CONTROLLER}/config/tita_stage2_controllers.yaml"
PREFLIGHT="${LOWLEVEL}/tita_low_level_sdk/stage2_production_preflight.py"
RL_TEST="${CONTROLLER}/test/test_rl_pipeline.cpp"
PLUGIN_TEST="${CONTROLLER}/test/test_controller_plugin.cpp"

[[ -f "${POLICY}" ]] || { echo "Missing policy: ${POLICY}" >&2; exit 1; }
for path in "${CONFIG}" "${PREFLIGHT}" "${RL_TEST}" "${PLUGIN_TEST}"; do
  [[ -f "${path}" ]] || { echo "Missing source: ${path}" >&2; exit 1; }
done

PYTHON=""
for candidate in "/home/cocel/venvs/cosim_ros2_jazzy/bin/python" python3; do
  if [[ -x "${candidate}" ]] && "${candidate}" -c 'import numpy, onnxruntime' 2>/dev/null; then
    PYTHON="${candidate}"
    break
  fi
done
[[ -n "${PYTHON}" ]] || { echo "Python with numpy+onnxruntime is required" >&2; exit 1; }

NEW_HASH="$(sha256sum "${POLICY}" | awk '{print $1}')"
OLD_HASH="$(awk '/^[[:space:]]*policy_sha256:/ {print $2; exit}' "${CONFIG}")"
echo "Policy: ${POLICY}"
echo "Old SHA256: ${OLD_HASH}"
echo "New SHA256: ${NEW_HASH}"

ACTION_JSON="$(${PYTHON} - "${POLICY}" <<'PY'
import json
import sys
import numpy as np
import onnxruntime as ort

s = ort.InferenceSession(sys.argv[1], providers=["CPUExecutionProvider"])
inputs = [(x.name, list(x.shape)) for x in s.get_inputs()]
outputs = [(x.name, list(x.shape)) for x in s.get_outputs()]
expected_inputs = [("nn_input0", [1, 33])]
expected_outputs = [("nn_output", [1, 8])]
if inputs != expected_inputs or outputs != expected_outputs:
    raise SystemExit(f"Policy interface mismatch: inputs={inputs}, outputs={outputs}")
action = s.run(
    ["nn_output"],
    {"nn_input0": np.zeros((1, 33), dtype=np.float32)},
)[0].reshape(-1)
if action.shape != (8,) or not np.isfinite(action).all():
    raise SystemExit("Policy zero-input action is invalid")
print(json.dumps([float(x) for x in action]))
PY
)"

ssh "${ROBOT}" '
  test "$(systemctl is-active tita-bringup.service)" = active
  test "$(ps -eo args= | awk '\''
    $0 !~ /awk/ && $0 ~ /direct_rl_controller_node|stage1_hardware.launch.py/ {count++}
    END {print count + 0}
  '\'')" = 0
'

mkdir -p "${BACKUP}"
rsync -a "${ROBOT}:~/tita_ws/policy/policy.onnx" "${BACKUP}/policy.onnx"
sha256sum "${BACKUP}/policy.onnx" > "${BACKUP}/SHA256SUMS"

"${PYTHON}" - "${NEW_HASH}" "${OLD_HASH}" "${ACTION_JSON}" \
  "${CONFIG}" "${PREFLIGHT}" "${RL_TEST}" "${PLUGIN_TEST}" <<'PY'
from pathlib import Path
import json
import re
import sys

new_hash, old_hash, action_json = sys.argv[1:4]
config, preflight, rl_test, plugin_test = map(Path, sys.argv[4:8])
if not re.fullmatch(r"[0-9a-f]{64}", new_hash):
    raise SystemExit("Invalid new SHA256")

text = config.read_text()
text, count = re.subn(
    r"(?m)^(\s*policy_sha256:\s*)[0-9a-f]{64}\s*$",
    rf"\g<1>{new_hash}", text, count=1)
if count != 1:
    raise SystemExit("Could not update controller policy hash")
config.write_text(text)

text = preflight.read_text()
text, count = re.subn(
    r'EXPECTED_POLICY_SHA256 = "[0-9a-f]{64}"',
    f'EXPECTED_POLICY_SHA256 = "{new_hash}"', text, count=1)
if count != 1:
    raise SystemExit("Could not update preflight policy hash")
preflight.write_text(text)

for path in (rl_test, plugin_test):
    text = path.read_text()
    text, count = re.subn(r'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])', new_hash, text)
    if count < 1:
        raise SystemExit(f"Policy test hash not found in {path}")
    path.write_text(text)

action = json.loads(action_json)
values = ", ".join(f"{value:.9g}F" for value in action)
text = rl_test.read_text()
pattern = (
    r'(TEST\(RlOnnx, FixedInterfaceHashAndOutputParity\).*?'
    r'const FloatJointArray expected = \{).*?(\};)'
)
text, count = re.subn(
    pattern, rf'\1\n    {values}\2', text, count=1, flags=re.DOTALL)
if count != 1:
    raise SystemExit("Could not update fixed-output parity fixture")
rl_test.write_text(text)
PY

rsync -a "${POLICY}" "${ROBOT}:~/tita_ws/policy/policy.onnx.new"
REMOTE_HASH="$(ssh "${ROBOT}" 'sha256sum ~/tita_ws/policy/policy.onnx.new' | awk '{print $1}')"
[[ "${REMOTE_HASH}" == "${NEW_HASH}" ]] || { echo "Remote policy hash mismatch" >&2; exit 1; }

rsync -a "${CONTROLLER}/" "${ROBOT}:~/tita_ws/src/tita_stage1_controller/"
rsync -a "${LOWLEVEL}/" "${ROBOT}:~/tita_ws/src/tita_low_level_sdk/"
ssh "${ROBOT}" 'mv ~/tita_ws/policy/policy.onnx.new ~/tita_ws/policy/policy.onnx'

ssh "${ROBOT}" 'bash -lc "
  set -e
  source /opt/ros/humble/setup.bash
  source /opt/tita/ros2/setup.bash
  cd /home/robot/tita_ws
  colcon build --packages-select tita_stage1_controller tita_low_level_sdk
  source install/setup.bash
  colcon test --packages-select tita_stage1_controller
  colcon test-result --test-result-base build/tita_stage1_controller --verbose
  colcon test --packages-select tita_low_level_sdk
  colcon test-result --test-result-base build/tita_low_level_sdk --verbose
  export ROS_DOMAIN_ID=42
  export ROS_LOCALHOST_ONLY=0
  ros2 run tita_low_level_sdk stage2_production_preflight \\
    --upstream /home/robot/tita_ws/src/ddt_ros2_control \\
    --install /home/robot/tita_ws/install \\
    --lowlevel /home/robot/tita_ws/src/tita_low_level_sdk \\
    --policy /home/robot/tita_ws/policy/policy.onnx \\
    --output /home/robot/tita_ws/runtime/stage2_preflight.json
"'

ssh "${ROBOT}" "python3 - <<'PY'
import json
from pathlib import Path
r = json.loads(Path('/home/robot/tita_ws/runtime/stage2_preflight.json').read_text())
assert r['ready'] is True, r
assert r['blockers'] == [], r
assert r['command_output'] == 'DISABLED', r
assert r['policy_sha256'] == '${NEW_HASH}', r
print('POLICY DEPLOYMENT PASS')
print('COMMAND OUTPUT: DISABLED')
PY"

echo "Backup: ${BACKUP}"
