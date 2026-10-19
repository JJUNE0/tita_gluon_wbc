#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: prepared source/build only; requires separate operator deployment approval.
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-18/leg_notch_validation"
cd "$workspace"
if pgrep -x tita_node >/dev/null; then echo 'Controller active; refusing deployment.' >&2; exit 3; fi
case ${1:-} in
 deploy_build)
    sha256sum -c "$stage/expected_before.sha256"
    test ! -e "$stage/before_deployment.tar.gz"
    tar -czf "$stage/before_deployment.tar.gz" README.md run_flashsac.sh src/tita_controller install/tita_controller
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
      --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3 2>&1 | tee "$stage/build.log"
    ;;
 verify)
    set +u
    source /opt/ros/humble/setup.bash
    source install/setup.bash
    set -u
    sha256sum -c "$stage/source_payload.sha256"
    for name in flashsac tita; do
      cmp "src/tita_controller/launch/$name.launch.py" "install/tita_controller/share/tita_controller/launch/$name.launch.py"
    done
    cmp run_flashsac.sh install/tita_controller/lib/tita_controller/run_flashsac.sh
    g++ -std=c++17 -O2 -Wall -Wextra -Werror -pedantic -I src/tita_controller/include \
      test/leg_action_filter/test_leg_action_filter.cpp -o test/leg_action_filter/filter_test
    test/leg_action_filter/filter_test
    /usr/bin/python3 - <<'PY'
import importlib.util
from pathlib import Path
from unittest.mock import patch
from launch import LaunchContext
from rclpy.serialization import serialize_message, deserialize_message
from tita_controller.msg import ActionFilterSample, TrainingSample
root=Path('/home/robot/tita_ws/install/tita_controller/share/tita_controller')
def load(name):
    spec=importlib.util.spec_from_file_location(name,root/'launch'/f'{name}.launch.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
public,generic=load('flashsac'),load('tita')
public.validate_policy(root/'policies/flashsac_80000')
params=generic.policy_parameters(root/'policies/flashsac_80000')
assert params['joint_kp']==[60.,60.,92.,0.,60.,60.,92.,0.]
assert params['joint_kd']==[1.5,1.5,2.3,.5,1.5,1.5,2.3,.5]
assert params['torque_limit']==[60.,60.,60.,12.,60.,60.,60.,12.]
for mode in ('none','ma2_legs','ma2_notch_legs'):
    context=LaunchContext()
    context.launch_configurations.update(output_enabled='false',namespace='tita4252763',
        policy_dir=str(root/'policies/flashsac_80000'),leg_action_filter=mode)
    with patch.object(public,'ExecuteProcess') as runner:
        public.setup(context)
        assert runner.call_args.kwargs['additional_env']['TITA_LEG_ACTION_FILTER']==mode
    with patch.object(generic,'Node',side_effect=lambda **kw:kw):
        nodes=generic.setup(context)
        assert nodes[1]['parameters'][0]['leg_action_filter']==mode
        assert nodes[1]['parameters'][0]['leg_notch_hz']==8.3
        assert nodes[1]['parameters'][0]['leg_notch_q']==3.
        assert not nodes[1]['parameters'][0]['output_enabled']
sample=ActionFilterSample()
sample.sequence_id=2**53+7;sample.monotonic_ns=2**63+20_000_000
sample.leg_action_filter='ma2_legs';sample.action_applied=[.5]*8
assert deserialize_message(serialize_message(sample),ActionFilterSample)==sample
assert 'action_raw' in TrainingSample.get_fields_and_field_types()
assert 'action_applied' not in TrainingSample.get_fields_and_field_types()
print('PASS ARM: installed pins/gains, all three launch modes without execution, message CDR/uint64; no nodes/SDK constructed')
PY
    ldd install/tita_controller/lib/tita_controller/tita_node > "$stage/linkage.log"
    if grep -q 'not found' "$stage/linkage.log"; then exit 4; fi
    strings install/tita_controller/lib/tita_controller/tita_node | grep 'leg notch:'
    strings install/tita_controller/lib/tita_controller/tita_node | grep 'shutdown zero-torque commands sent'
    sha256sum install/tita_controller/lib/tita_controller/tita_node > "$stage/executable_after.sha256"
    if pgrep -x tita_node >/dev/null; then exit 3; fi
    echo 'PASS ROBOT_COMMAND_FREE_RUNTIME: rebuilt ARM binary and filter/launch/message verification; motors not run.'
    ;;
 *) echo 'Usage: deploy_leg_notch.sh deploy_build|verify' >&2; exit 2 ;;
esac
