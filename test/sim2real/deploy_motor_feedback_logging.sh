#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: operator-authorized workspace deployment and build only.
# Does not launch a node, stop services, open CAN or command hardware.
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-17/motor_feedback_logging"
cd "$workspace"
guard_unused_package() {
    /usr/bin/python3 - <<'PY'
from pathlib import Path
for proc in Path('/proc').iterdir():
    if not proc.name.isdigit():
        continue
    try:
        args = (proc / 'cmdline').read_bytes().split(b'\0')
        if any(Path(a.decode(errors='replace')).name == 'tita_node' for a in args if a):
            raise SystemExit('Refusing deployment: tita_node is running: '+proc.name)
        if '/home/robot/tita_ws/install/tita_controller/' in (proc / 'maps').read_text():
            raise SystemExit('Refusing deployment: package is loaded by PID '+proc.name)
    except (FileNotFoundError, ProcessLookupError, PermissionError):
        pass
print('PASS workspace controller package unused; default /opt bringup left running')
PY
}
guard_unused_package
case ${1:-} in
    deploy_build)
        sha256sum -c "$stage/expected_before.sha256"
        test ! -e src/tita_controller/msg/MotorFeedback.msg
        test ! -e "$stage/before_deployment.tar.gz"
        sha256sum -c "$stage/payload.sha256"
        tar -czf "$stage/before_deployment.tar.gz" \
            src/tita_controller README.md run_flashsac.sh install/tita_controller
        sha256sum "$stage/before_deployment.tar.gz" > "$stage/backup.sha256"
        guard_unused_package
        tar -xzf "$stage/payload.tar.gz" -C "$workspace"
        sha256sum -c "$stage/source_payload.sha256"
        guard_unused_package
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
        sha256sum -c "$stage/preserved.sha256"
        cmp run_flashsac.sh install/tita_controller/lib/tita_controller/run_flashsac.sh
        cmp src/tita_controller/msg/MotorFeedback.msg \
            install/tita_controller/share/tita_controller/msg/MotorFeedback.msg
        ldd install/tita_controller/lib/tita_controller/tita_node > "$stage/linkage.log"
        if grep -q 'not found' "$stage/linkage.log"; then exit 4; fi
        /usr/bin/python3 - <<'PY'
import importlib.util
import unittest
from pathlib import Path
root = Path('/home/robot/tita_ws')
spec = importlib.util.spec_from_file_location('feedback_test', root / 'test/motor_feedback_logging/test_training_logging.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.REPO = root
suite = unittest.TestSuite(module.TrainingLoggingTest(name) for name in (
    'test_feedback_bag_join_keeps_previous_command_and_invalid_reads',
    'test_sqlite_round_trip_preserves_atomic_frames_and_integer_times'))
result = unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful():
    raise SystemExit(1)
print('ROBOT_COMMAND_FREE_RUNTIME PASS: ARM/Humble CDR/SQLite only; no nodes or SDK instantiated')
PY
        sha256sum install/tita_controller/lib/tita_controller/tita_node \
            install/tita_controller/lib/tita_controller/run_flashsac.sh \
            install/tita_controller/share/tita_controller/msg/MotorFeedback.msg \
            > "$stage/installed.sha256"
        guard_unused_package
        echo 'PASS feedback logging deployed/built; no controller or motor command executed.'
        ;;
    *) echo 'Usage: deploy_motor_feedback_logging.sh deploy_build|verify' >&2; exit 2 ;;
esac
