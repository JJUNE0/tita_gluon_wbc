#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: explicitly authorized source deployment/build only.
# No robot controller execution, service changes, MCU mode or CAN commands.
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-18/slow_sit_80000_deploy"
cd "$workspace"
if pgrep -x tita_node >/dev/null; then
    echo 'Refusing deployment/build while tita_node runs.' >&2
    exit 3
fi
case ${1:-} in
    deploy_build)
        sha256sum -c "$stage/expected_before.sha256"
        test ! -e "$stage/before_deployment.tar.gz"
        test ! -e src/tita_controller/include/tita_controller/supporting_sit.hpp
        test ! -e src/tita_controller/include/tita_controller/sit_geometry.hpp
        test ! -e src/tita_controller/policies/flashsac_80000
        tar -czf "$stage/before_deployment.tar.gz" \
            src/tita_controller/include/tita_controller/state_machine.hpp \
            src/tita_controller/src/tita_node.cpp src/tita_controller/launch/flashsac.launch.py \
            run_flashsac.sh README.md install/tita_controller
        sha256sum "$stage/before_deployment.tar.gz" > "$stage/backup.sha256"
        sha256sum -c "$stage/payload.sha256"
        tar -xzf "$stage/payload.tar.gz" -C "$workspace"
        sha256sum -c "$stage/source_payload.sha256"
        if pgrep -x tita_node >/dev/null; then exit 3; fi
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
        ldd install/tita_controller/lib/tita_controller/tita_node > "$stage/linkage.log"
        if grep -q 'not found' "$stage/linkage.log"; then exit 4; fi
        /usr/bin/python3 - <<'PY'
from pathlib import Path
import importlib.util
root=Path('/home/robot/tita_ws/install/tita_controller/share/tita_controller')
for name in ('flashsac','tita'):
    spec=importlib.util.spec_from_file_location(name,root/'launch'/f'{name}.launch.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if name=='flashsac':module.validate_policy(root/'policies/flashsac_80000')
    else:
        params=module.policy_parameters(root/'policies/flashsac_80000')
        assert len(params['obs_kind'])==33 and len(params['action_joint'])==8
        assert params['max_lin_x']==params['max_ang_z']==1.
        module.velocity_bias_parameters(root/'policies/flashsac_80000',1.)
print('PASS installed bundle/launch hashes, obs33/action8, command +/-1; no node instantiated')
PY
        mkdir -p test/slow_sit_80000
        for name in joystick_buttons_runtime supporting_sit_replay; do
            g++ -std=c++17 -O2 -Wall -Wextra -Werror -pedantic -I src/tita_controller/include \
                "test/slow_sit_80000/$name.cpp" -o "test/slow_sit_80000/$name"
        done
        test/slow_sit_80000/joystick_buttons_runtime | tee "$stage/arm_buttons.log"
        test/slow_sit_80000/supporting_sit_replay < test/slow_sit_80000/replay_input.txt > "$stage/arm_replay_actual.txt"
        /usr/bin/python3 - <<'PY'
from pathlib import Path
root=Path('/home/robot/tita_ws')
expected=[list(map(float,x.split())) for x in (root/'test/slow_sit_80000/replay_expected.txt').read_text().splitlines()]
actual=[list(map(float,x.split())) for x in (root/'docs/exp/2026-10-18/slow_sit_80000_deploy/arm_replay_actual.txt').read_text().splitlines()]
assert len(expected)==len(actual)==1000
assert all(len(a)==len(e)==9 for a,e in zip(actual,expected))
error=max(abs(a-e) for aa,ee in zip(actual,expected) for a,e in zip(aa,ee))
assert error<1e-9,error
print('PASS ARM math replay: 1000 cases, maximum absolute error',error)
PY
        sha256sum install/tita_controller/lib/tita_controller/tita_node \
            install/tita_controller/lib/tita_controller/run_flashsac.sh > "$stage/installed.sha256"
        if pgrep -x tita_node >/dev/null; then exit 5; fi
        echo 'PASS ROBOT_STATE_CHANGING: installed and rebuilt; no controller or torque execution.'
        ;;
    *) echo 'Usage: deploy_supporting_sit_80000.sh deploy_build|verify' >&2; exit 2 ;;
esac
