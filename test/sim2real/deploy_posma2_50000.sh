#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: operator-requested policy/support-code install and build only.
# ROBOT_COMMAND_FREE_RUNTIME: verify uses pure ONNX/launch imports; no SDK, CAN or ROS nodes.
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-18/flashsac_posma2_50000_deployment"
cd "$workspace"
guard_unused_overlay() {
    if pgrep -f '^/home/robot/tita_ws/install/(tita_controller|teleop_command)/lib/' >/dev/null; then
        echo 'Refusing to overwrite an overlay with its controller or joystick running.' >&2
        exit 3
    fi
    # The vendor service uses /opt/tita, not this overlay. Do not stop or restart it.
}
guard_unused_overlay
case ${1:-} in
deploy_build)
    sha256sum -c "$stage/expected_before.sha256"
    sha256sum -c "$stage/payload.sha256"
    test ! -e src/tita_controller/policies/flashsac_posma2_50000
    test ! -e "$stage/before_deployment.tar.gz"
    systemctl show tita-bringup.service --property=MainPID --property=ActiveState \
        --property=ExecMainStartTimestampMonotonic > "$stage/service_before.txt"
    tar -czf "$stage/before_deployment.tar.gz" src/tita_controller run_flashsac.sh README.md install/tita_controller
    sha256sum "$stage/before_deployment.tar.gz" > "$stage/backup.sha256"
    guard_unused_overlay
    tar -xzf "$stage/payload.tar.gz" -C "$workspace" --no-same-owner
    sha256sum -c "$stage/source_payload.sha256"
    set +u
    source /opt/ros/humble/setup.bash
    source install/setup.bash
    set -u
    CMAKE_BUILD_PARALLEL_LEVEL=2 MAKEFLAGS=-j2 colcon --log-base "$stage/colcon" build \
        --executor sequential --packages-select tita_controller \
        --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3 \
        2>&1 | tee "$stage/build.log"
    ;;
verify)
    set +u
    source /opt/ros/humble/setup.bash
    source install/setup.bash
    set -u
    export ROS_LOG_DIR="$stage/ros_import_checks"
    sha256sum -c "$stage/source_payload.sha256"
    cmp run_flashsac.sh install/tita_controller/lib/tita_controller/run_flashsac.sh
    for name in flashsac tita; do
        cmp "src/tita_controller/launch/$name.launch.py" \
            "install/tita_controller/share/tita_controller/launch/$name.launch.py"
    done
    for name in policy.onnx config.json manifest.json; do
        cmp "src/tita_controller/policies/flashsac_posma2_50000/$name" \
            "install/tita_controller/share/tita_controller/policies/flashsac_posma2_50000/$name"
    done
    /usr/bin/python3 test/posma2_50000/check_posma2_50000_launch.py \
        install/tita_controller/share/tita_controller | tee "$stage/launch_check.log"
    ort=build/tita_controller/_deps/onnxruntime-src
    g++ -std=c++17 -O2 -I "$ort/include" test/posma2_50000/inference.cpp \
        -L "$ort/lib" -Wl,-rpath,"$workspace/$ort/lib" -lonnxruntime \
        -o test/posma2_50000/inference
    test/posma2_50000/inference \
        install/tita_controller/share/tita_controller/policies/flashsac_posma2_50000/policy.onnx \
        test/posma2_50000/obs.txt > "$stage/arm_actual.txt"
    /usr/bin/python3 - <<'PY'
import json
from pathlib import Path
import numpy as np
stage = Path('docs/exp/2026-10-18/flashsac_posma2_50000_deployment')
actual = np.loadtxt(stage / 'arm_actual.txt')
expected = np.load('test/posma2_50000/expected.npy')
assert actual.shape == expected.shape == (256, 8)
np.testing.assert_allclose(actual, expected, rtol=1e-4, atol=2e-5)
result = dict(execution_domain='ROBOT_COMMAND_FREE_RUNTIME', evidence_status='PASS',
    checkpoint_sha256='baba6974b76d4e8a7b7107cdfab9d2b7bb73695df00419009279549ebd51f992',
    samples=len(actual), max_abs_error=float(abs(actual - expected).max()))
(stage / 'arm_parity.json').write_text(json.dumps(result, indent=2) + '\n')
print(result)
PY
    ldd install/tita_controller/lib/tita_controller/tita_node > "$stage/linkage.log"
    if grep -q 'not found' "$stage/linkage.log"; then exit 4; fi
    systemctl show tita-bringup.service --property=MainPID --property=ActiveState \
        --property=ExecMainStartTimestampMonotonic > "$stage/service_after.txt"
    cmp "$stage/service_before.txt" "$stage/service_after.txt"
    sha256sum install/tita_controller/lib/tita_controller/tita_node \
        install/tita_controller/lib/tita_controller/run_flashsac.sh \
        install/tita_controller/share/tita_controller/launch/*.py \
        install/tita_controller/share/tita_controller/policies/flashsac_posma2_50000/* \
        > "$stage/installed.sha256"
    guard_unused_overlay
    echo 'PASS ROBOT_STATE_CHANGING: build/install verified. Vendor service PID unchanged; no controller or motor command executed.'
    ;;
*) echo 'Usage: deploy_posma2_50000.sh deploy_build|verify' >&2; exit 2 ;;
esac
