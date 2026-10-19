#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: operator-approved (2026-10-18) resource deployment/build of the selectable
# flashsac_c2_60000 bundle. Never runs the controller, services, MCU mode requests or motors.
# verify runs ONNX inference without ROS nodes, CAN or SDK (ROBOT_COMMAND_FREE_RUNTIME).
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-18/flashsac_c2_60000_deploy"
cd "$workspace"
guard_idle() {
    if pgrep -f '(^|/)(ros2_control_node|tita_node|teleop_command_node)( |$)' >/dev/null; then
        echo 'Refusing deployment while a controller or joystick is running.' >&2
        exit 3
    fi
    local state
    state=$(systemctl is-active tita-bringup.service || true)
    case $state in inactive|failed|unknown) ;; *) echo "Bringup is $state; refusing deployment." >&2; exit 3 ;; esac
}
guard_idle
case ${1:-} in
    deploy_build)
        sha256sum -c "$stage/expected_before.sha256"
        test ! -e src/tita_controller/policies/flashsac_c2_60000
        test ! -e test/flashsac_c2_60000
        test ! -e "$stage/before_deployment.tar.gz"
        sha256sum -c "$stage/payload.sha256"
        tar -czf "$stage/before_deployment.tar.gz" README.md run_flashsac.sh \
            src/tita_controller/launch/flashsac.launch.py \
            install/tita_controller/lib/tita_controller/run_flashsac.sh \
            install/tita_controller/share/tita_controller/launch/flashsac.launch.py
        sha256sum "$stage/before_deployment.tar.gz" > "$stage/backup.sha256"
        sha256sum install/tita_controller/lib/tita_controller/tita_node > "$stage/executable_before.sha256"
        guard_idle
        tar -xzf "$stage/payload.tar.gz" -C "$workspace" --no-same-owner
        sha256sum -c "$stage/source_payload.sha256"
        guard_idle
        set +u
        source /opt/ros/humble/setup.bash
        source install/setup.bash
        set -u
        colcon --log-base "$stage/colcon" build --packages-select tita_controller \
            --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3 \
            2>&1 | tee "$stage/build.log"
        ;;
    verify)
        set +u
        source /opt/ros/humble/setup.bash
        source install/setup.bash
        set -u
        sha256sum -c "$stage/source_payload.sha256"
        cmp run_flashsac.sh install/tita_controller/lib/tita_controller/run_flashsac.sh
        cmp src/tita_controller/launch/flashsac.launch.py install/tita_controller/share/tita_controller/launch/flashsac.launch.py
        for name in policy.onnx config.json manifest.json; do
            cmp "src/tita_controller/policies/flashsac_c2_60000/$name" \
                "install/tita_controller/share/tita_controller/policies/flashsac_c2_60000/$name"
            cmp "src/tita_controller/policies/flashsac_80000/$name" \
                "install/tita_controller/share/tita_controller/policies/flashsac_80000/$name"
        done
        /usr/bin/python3 - <<'PY'
import importlib.util
from pathlib import Path
root = Path('/home/robot/tita_ws/install/tita_controller/share/tita_controller')
def load(name):
    spec = importlib.util.spec_from_file_location(name, root / 'launch' / f'{name}.launch.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
flashsac, tita = load('flashsac'), load('tita')
for bundle in ('flashsac_80000', 'flashsac_c2_60000'):
    flashsac.validate_policy(root / 'policies' / bundle)
p = tita.policy_parameters(root / 'policies/flashsac_c2_60000')
assert p['joint_kp'] == [60., 60., 60., 0., 60., 60., 60., 0.]
assert p['joint_kd'] == [1.5, 1.5, 1.5, .5, 1.5, 1.5, 1.5, .5]
assert p['torque_limit'] == [60., 60., 60., 12., 60., 60., 60., 12.]
assert len(p['obs_kind']) == 33 and len(p['action_joint']) == 8 and p['policy_dt'] == .02
assert p['max_lin_x'] == 1. and p['max_ang_z'] == 1.
q = tita.policy_parameters(root / 'policies/flashsac_80000')
assert q['joint_kp'] == [60., 60., 92., 0., 60., 60., 92., 0.]
print('PASS installed bundles: flashsac_c2_60000 legs 60/1.5, wheel 0.5, caps 60/12, 33 obs, 8 actions, 50 Hz; '
      'flashsac_80000 unchanged (knee 92/2.3); no nodes constructed')
PY
        ort=build/tita_controller/_deps/onnxruntime-src
        g++ -std=c++17 -O2 -I src/tita_controller/include -I "$ort/include" \
            test/flashsac_c2_60000/flashsac_runtime.cpp -L "$ort/lib" \
            -Wl,-rpath,"$workspace/$ort/lib" -lonnxruntime -o test/flashsac_c2_60000/inference
        test/flashsac_c2_60000/inference \
            install/tita_controller/share/tita_controller/policies/flashsac_c2_60000/policy.onnx \
            test/flashsac_c2_60000/obs.txt > "$stage/runtime_actual.txt"
        /usr/bin/python3 - <<'PY'
import json
from pathlib import Path
import numpy as np
root = Path('/home/robot/tita_ws')
stage = root / 'docs/exp/2026-10-18/flashsac_c2_60000_deploy'
actual = np.loadtxt(stage / 'runtime_actual.txt')
expected = np.load(root / 'test/flashsac_c2_60000/expected.npy')
np.testing.assert_allclose(actual, expected, rtol=1e-4, atol=2e-5)
result = dict(execution_domain='ROBOT_COMMAND_FREE_RUNTIME', evidence_status='PASS',
              checkpoint_sha256='b4c8ae072787c3119864e75c2ebfbaf8284a02976dc68f1f282ad9480ae2e116',
              samples=len(actual), max_action_error=float(abs(actual - expected).max()))
(stage / 'runtime_parity.json').write_text(json.dumps(result, indent=2) + '\n')
print(result)
PY
        sha256sum install/tita_controller/lib/tita_controller/tita_node > "$stage/executable_after.sha256"
        cmp "$stage/executable_before.sha256" "$stage/executable_after.sha256"
        sha256sum install/tita_controller/lib/tita_controller/run_flashsac.sh \
            install/tita_controller/share/tita_controller/launch/flashsac.launch.py \
            install/tita_controller/share/tita_controller/policies/flashsac_c2_60000/* > "$stage/installed.sha256"
        guard_idle
        echo 'PASS ROBOT_STATE_CHANGING: flashsac_c2_60000 installed; executable unchanged; no controller, service, MCU or motor command executed.'
        ;;
    *) echo 'Usage: deploy_flashsac_c2_60000.sh deploy_build|verify' >&2; exit 2 ;;
esac
