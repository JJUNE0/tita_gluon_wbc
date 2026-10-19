#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: operator-authorized policy deployment/build only.
# verify runs inference without ROS nodes, CAN, SDK or motor commands.
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-17/flashsac_50000_deployment"
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
        test ! -e src/tita_controller/policies/flashsac_50000
        test ! -e "$stage/before_deployment.tar.gz"
        sha256sum -c "$stage/payload.sha256"
        tar -czf "$stage/before_deployment.tar.gz" \
            src/tita_controller/launch/flashsac.launch.py run_flashsac.sh README.md \
            src/tita_controller/policies/flashsac_60000 install/tita_controller
        sha256sum "$stage/before_deployment.tar.gz" > "$stage/backup.sha256"
        guard_idle
        tar -xzf "$stage/payload.tar.gz" -C "$workspace"
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
        for name in policy.onnx config.json; do
            cmp "src/tita_controller/policies/flashsac_50000/$name" \
                "install/tita_controller/share/tita_controller/policies/flashsac_50000/$name"
        done
        # Confirm the former bundle remains available and byte-for-byte intact.
        printf '%s\n' \
            'f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a  src/tita_controller/policies/flashsac_60000/policy.onnx' \
            'd429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d  src/tita_controller/policies/flashsac_60000/config.json' | sha256sum -c -
        /usr/bin/python3 - <<'PY'
import importlib.util
from pathlib import Path
root = Path('/home/robot/tita_ws/install/tita_controller/share/tita_controller')
bundle = root / 'policies/flashsac_50000'
for name in ('flashsac', 'tita'):
    spec = importlib.util.spec_from_file_location(name, root / 'launch' / f'{name}.launch.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if name == 'flashsac':
        module.validate_policy(bundle)
    else:
        params = module.policy_parameters(bundle)
        assert len(params['action_joint']) == 8 and len(params['obs_kind']) == 33
        assert params['policy_dt'] == .02
        assert params['max_lin_x'] == 1. and params['max_ang_z'] == 1.
        module.velocity_bias_parameters(bundle, 1.)
print('PASS installed launch/bundle/hash/33 observations/8 actions/50 Hz; no nodes constructed')
PY
        ldd install/tita_controller/lib/tita_controller/tita_node > "$stage/linkage.log"
        if grep -q 'not found' "$stage/linkage.log"; then exit 4; fi
        ort=build/tita_controller/_deps/onnxruntime-src
        g++ -std=c++17 -O2 -I src/tita_controller/include -I "$ort/include" \
            test/flashsac_50000/flashsac_runtime.cpp -L "$ort/lib" \
            -Wl,-rpath,"$workspace/$ort/lib" -lonnxruntime -o test/flashsac_50000/inference
        test/flashsac_50000/inference \
            install/tita_controller/share/tita_controller/policies/flashsac_50000/policy.onnx \
            test/flashsac_50000/obs.txt > "$stage/arm_actual.txt"
        /usr/bin/python3 - <<'PY'
import json
from pathlib import Path
import numpy as np
root = Path('/home/robot/tita_ws')
actual = np.loadtxt(root / 'docs/exp/2026-10-17/flashsac_50000_deployment/arm_actual.txt')
expected = np.load(root / 'test/flashsac_50000/expected.npy')
np.testing.assert_allclose(actual, expected, rtol=1e-4, atol=2e-5)
result = dict(execution_domain='ROBOT_COMMAND_FREE_RUNTIME', evidence_status='PASS',
              checkpoint_sha256='d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c',
              samples=len(actual), max_action_error=float(abs(actual - expected).max()))
(root / 'docs/exp/2026-10-17/flashsac_50000_deployment/arm_parity.json').write_text(json.dumps(result, indent=2) + '\n')
print(result)
PY
        sha256sum install/tita_controller/lib/tita_controller/tita_node \
            install/tita_controller/lib/tita_controller/run_flashsac.sh \
            install/tita_controller/share/tita_controller/policies/flashsac_50000/policy.onnx \
            install/tita_controller/share/tita_controller/policies/flashsac_50000/config.json \
            > "$stage/installed.sha256"
        guard_idle
        echo 'PASS installed model_50000; no controller, service, MCU or motor command executed.'
        ;;
    *) echo 'Usage: deploy_flashsac_50000.sh deploy_build|verify' >&2; exit 2 ;;
esac
