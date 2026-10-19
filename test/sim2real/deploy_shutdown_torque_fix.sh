#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: separately approved source/build deployment only.
# Does not release existing motor torque, run a controller or change MCU/service mode.
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-18/flashsac_shutdown_torque_fix"
cd "$workspace"
if pgrep -x tita_node >/dev/null; then echo 'Controller active; refusing deployment.' >&2; exit 3; fi
case ${1:-} in
 deploy_build)
    sha256sum -c "$stage/expected_before.sha256"
    test ! -e src/tita_controller/include/tita_controller/control_loop_exit.hpp
    test ! -e "$stage/before_deployment.tar.gz"
    tar -czf "$stage/before_deployment.tar.gz" README.md src/tita_controller/src/tita_node.cpp install/tita_controller
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
    sha256sum -c "$stage/source_payload.sha256"
    set +u
    source /opt/ros/humble/setup.bash
    source install/setup.bash
    set -u
    g++ -std=c++17 -O2 -pthread -Wall -Wextra -Werror -pedantic \
        -I src/tita_controller/include test/shutdown_torque_fix/test_control_loop_exit.cpp \
        -o test/shutdown_torque_fix/test_control_loop_exit
    test/shutdown_torque_fix/test_control_loop_exit
    ldd install/tita_controller/lib/tita_controller/tita_node > "$stage/linkage.log"
    if grep -q 'not found' "$stage/linkage.log"; then exit 4; fi
    strings install/tita_controller/lib/tita_controller/tita_node | grep 'shutdown zero-torque commands sent'
    sha256sum install/tita_controller/lib/tita_controller/tita_node > "$stage/executable_after.sha256"
    if pgrep -x tita_node >/dev/null; then exit 3; fi
    echo 'PASS: rebuilt binary and ARM mock release tests; robot controller NOT executed.'
    ;;
 *) echo 'Usage: deploy_shutdown_torque_fix.sh deploy_build|verify' >&2; exit 2 ;;
esac
