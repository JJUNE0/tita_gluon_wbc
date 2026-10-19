#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: operator-approved resource update/build only, never run motors.
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-18/flashsac_80000_leg_pd_92_23"
cd "$workspace"
if pgrep -x tita_node >/dev/null; then
    echo 'Refusing resource replacement while FlashSAC tita_node runs.' >&2; exit 3
fi
case ${1:-} in
 deploy_build)
    sha256sum -c "$stage/expected_before.sha256"
    test ! -e "$stage/before_deployment.tar.gz"
    tar -czf "$stage/before_deployment.tar.gz" README.md \
        src/tita_controller/launch/flashsac.launch.py \
        src/tita_controller/policies/flashsac_80000/config.json \
        src/tita_controller/policies/flashsac_80000/manifest.json \
        install/tita_controller/share/tita_controller/launch/flashsac.launch.py \
        install/tita_controller/share/tita_controller/policies/flashsac_80000/config.json \
        install/tita_controller/share/tita_controller/policies/flashsac_80000/manifest.json
    sha256sum "$stage/before_deployment.tar.gz" > "$stage/backup.sha256"
    sha256sum install/tita_controller/lib/tita_controller/tita_node > "$stage/executable_before.sha256"
    sha256sum -c "$stage/payload.sha256"
    tar -xzf "$stage/payload.tar.gz" -C "$workspace"
    sha256sum -c "$stage/source_payload.sha256"
    if pgrep -x tita_node >/dev/null; then exit 3; fi
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
    cmp src/tita_controller/launch/flashsac.launch.py install/tita_controller/share/tita_controller/launch/flashsac.launch.py
    cmp src/tita_controller/policies/flashsac_80000/config.json install/tita_controller/share/tita_controller/policies/flashsac_80000/config.json
    cmp src/tita_controller/policies/flashsac_80000/manifest.json install/tita_controller/share/tita_controller/policies/flashsac_80000/manifest.json
    /usr/bin/python3 - <<'PY'
from pathlib import Path
import importlib.util
root=Path('/home/robot/tita_ws/install/tita_controller/share/tita_controller')
def load(name):
    spec=importlib.util.spec_from_file_location(name,root/'launch'/f'{name}.launch.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
load('flashsac').validate_policy(root/'policies/flashsac_80000')
p=load('tita').policy_parameters(root/'policies/flashsac_80000')
assert p['joint_kp']==[92.,92.,92.,0.,92.,92.,92.,0.]
assert p['joint_kd']==[2.3,2.3,2.3,.5,2.3,2.3,2.3,.5]
assert p['torque_limit']==[60.,60.,60.,12.,60.,60.,60.,12.]
print('PASS installed policy hashes / RL leg Kp92 Kd2.3 / wheel and torque caps unchanged; no nodes constructed')
PY
    sha256sum install/tita_controller/lib/tita_controller/tita_node > "$stage/executable_after.sha256"
    cmp "$stage/executable_before.sha256" "$stage/executable_after.sha256"
    if pgrep -x tita_node >/dev/null; then exit 3; fi
    echo 'PASS ROBOT_STATE_CHANGING: resource installation verified; executable unchanged; motors not run.'
    ;;
 *) echo 'Usage: deploy_leg_pd_92_23.sh deploy_build|verify' >&2; exit 2 ;;
esac
