#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: explicitly requested source deployment/build only.
# No controller execution, service changes, MCU/CAN commands or robot motion.
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-17/velocity_bias_08nm_deployment"
cd "$workspace"
if pgrep -x tita_node >/dev/null; then
    echo 'Refusing deployment/build while tita_node is running.' >&2
    exit 3
fi
case ${1:-} in
    deploy_build)
        sha256sum -c "$stage/expected_before.sha256"
        test ! -e "$stage/before_deployment.tar.gz"
        tar -czf "$stage/before_deployment.tar.gz" \
            src/tita_controller/include/tita_controller/velocity_bias.hpp \
            src/tita_controller/src/tita_node.cpp \
            src/tita_controller/launch/flashsac.launch.py \
            src/tita_controller/launch/tita.launch.py run_flashsac.sh README.md install/tita_controller
        sha256sum "$stage/before_deployment.tar.gz" > "$stage/backup.sha256"
        sha256sum -c "$stage/payload.sha256"
        tar -xzf "$stage/payload.tar.gz" -C "$workspace"
        sha256sum -c "$stage/source_payload.sha256"
        if pgrep -x tita_node >/dev/null; then
            echo 'Controller started during preparation; refusing build/install.' >&2
            exit 3
        fi
        # Source only environment hooks, never the public robot runner.
        set +u
        source /opt/ros/humble/setup.bash
        source install/setup.bash
        set -u
        colcon --log-base "$stage/colcon" build --packages-select tita_controller \
            --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3 2>&1 | tee "$stage/build.log"
        ;;
    verify)
        set +u
        source /opt/ros/humble/setup.bash
        source install/setup.bash
        set -u
        sha256sum -c "$stage/source_payload.sha256"
        cmp run_flashsac.sh install/tita_controller/lib/tita_controller/run_flashsac.sh
        cmp src/tita_controller/launch/flashsac.launch.py install/tita_controller/share/tita_controller/launch/flashsac.launch.py
        cmp src/tita_controller/launch/tita.launch.py install/tita_controller/share/tita_controller/launch/tita.launch.py
        printf '%s\n' \
            'f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a  install/tita_controller/share/tita_controller/policies/flashsac_60000/policy.onnx' \
            'd429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d  install/tita_controller/share/tita_controller/policies/flashsac_60000/config.json' | sha256sum -c -
        ldd install/tita_controller/lib/tita_controller/tita_node > "$stage/linkage.log"
        if grep -q 'not found' "$stage/linkage.log"; then exit 4; fi
        g++ -std=c++17 -O2 -Wall -Wextra -Werror -pedantic -isystem /usr/include/eigen3 \
            -I src/tita_controller/include test/velocity_bias_08nm/velocity_bias_runtime.cpp \
            -o test/velocity_bias_08nm/math_runtime
        test/velocity_bias_08nm/math_runtime status < test/velocity_bias_08nm/arm_replay_input.txt \
            > "$stage/arm_replay_actual.txt"
        /usr/bin/python3 - <<'PY'
import importlib.util
from pathlib import Path
root = Path('/home/robot/tita_ws/install/tita_controller/share/tita_controller')
for name in ('flashsac', 'tita'):
    spec = importlib.util.spec_from_file_location(name, root/'launch'/f'{name}.launch.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if name == 'flashsac':
        module.validate_policy(root/'policies/flashsac_60000')
    else:
        params = module.policy_parameters(root/'policies/flashsac_60000')
        assert len(params['action_joint']) == 8 and len(params['obs_kind']) == 33
        module.velocity_bias_parameters(root/'policies/flashsac_60000', 1.)
print('PASS installed launch/pinned bundle/33 observations/8 actions; no nodes constructed')
PY
        sha256sum install/tita_controller/lib/tita_controller/tita_node \
            install/tita_controller/lib/tita_controller/run_flashsac.sh > "$stage/installed.sha256"
        if pgrep -x tita_node >/dev/null; then exit 5; fi
        printf '%s\n' 'PASS ARM pure-math replay executed; controller was not executed.'
        ;;
    *) echo 'Usage: deploy_velocity_bias_08nm.sh deploy_build|verify' >&2; exit 2 ;;
esac
