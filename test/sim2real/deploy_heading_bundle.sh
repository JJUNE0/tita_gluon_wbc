#!/usr/bin/env bash
# Runs ON THE ROBOT from ~/tita_ws. Operator-authorized (2026-10-19) code/bundle installation and build only.
# ROBOT_STATE_CHANGING: replaces tita_controller sources (heading_error observation + gyro bias), adds the
#   flashsac_headw0_50000 bundle, colcon-builds tita_controller. Backup first. Never starts the controller,
#   SDK, ROS nodes or CAN; never touches tita-bringup.service.
# ROBOT_COMMAND_FREE_RUNTIME (verify): launch-definition imports, pure ONNX inference, header-only C++ parity.
# Usage: [TITA_HEADING_BUNDLE=flashsac_headw0_<step> TITA_HEADING_STAGE=<dir>] deploy_heading_bundle.sh deploy_build|verify
set -euo pipefail
workspace=/home/robot/tita_ws
bundle=${TITA_HEADING_BUNDLE:-flashsac_headw0_50000}
stage="$workspace/docs/exp/2026-10-19/${TITA_HEADING_STAGE:-heading_bundle_deployment}"
fixtures=test/sim2real/heading_bundle
cd "$workspace"
guard_unused_overlay() {
    if pgrep -f '^/home/robot/tita_ws/install/(tita_controller|teleop_command)/lib/' >/dev/null; then
        echo 'Overlay controller/joystick is running; refusing deployment.' >&2
        exit 3
    fi
}
guard_unused_overlay
case ${1:-} in
deploy_build)
    sha256sum -c "$stage/expected_before.sha256"
    sha256sum -c "$stage/payload.sha256"
    test ! -e "src/tita_controller/policies/$bundle"
    test ! -e "$stage/before_deployment.tar.gz"
    systemctl show tita-bringup.service --property=MainPID --property=ActiveState \
        --property=ExecMainStartTimestampMonotonic > "$stage/service_before.txt"
    sha256sum install/tita_controller/lib/tita_controller/tita_node > "$stage/executable_before.sha256"
    tar -czf "$stage/before_deployment.tar.gz" src/tita_controller run_flashsac.sh install/tita_controller
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
    grep -q 'Finished <<< tita_controller' "$stage/build.log"
    ;;
verify)
    set +u
    source /opt/ros/humble/setup.bash
    source install/setup.bash
    set -u
    export ROS_LOG_DIR="$stage/ros_import_checks"
    sha256sum -c "$stage/source_payload.sha256"
    share=install/tita_controller/share/tita_controller
    cmp run_flashsac.sh install/tita_controller/lib/tita_controller/run_flashsac.sh
    for f in flashsac.launch.py tita.launch.py; do cmp "src/tita_controller/launch/$f" "$share/launch/$f"; done
    for name in policy.onnx config.json manifest.json; do
        cmp "src/tita_controller/policies/$bundle/$name" "$share/policies/$bundle/$name"
    done
    ort=build/tita_controller/_deps/onnxruntime-src
    g++ -std=c++17 -O2 -I "$ort/include" "$fixtures/inference.cpp" \
        -L "$ort/lib" -Wl,-rpath,"$workspace/$ort/lib" -lonnxruntime -o "$stage/inference"
    "$stage/inference" "$share/policies/$bundle/policy.onnx" "$fixtures/$bundle/obs.txt" > "$stage/inference_actual.txt"
    g++ -std=c++17 -O2 -Wall -Wextra -I src/tita_controller/include test/sim2real/checkpoint_heading_parity.cpp \
        -o "$stage/heading_parity"
    "$stage/heading_parity" < "$fixtures/$bundle/heading_parity_input.txt" > "$stage/heading_parity_actual.txt"
    /usr/bin/python3 test/sim2real/verify_heading_bundle.py "$share" "$fixtures" \
        --inference "$stage/inference_actual.txt" --parity "$stage/heading_parity_actual.txt" \
        --result "$stage/arm_verify.json" --bundle "$bundle" | tee "$stage/verify.log"
    ldd install/tita_controller/lib/tita_controller/tita_node > "$stage/linkage.log"
    if grep -q 'not found' "$stage/linkage.log"; then exit 4; fi
    systemctl show tita-bringup.service --property=MainPID --property=ActiveState \
        --property=ExecMainStartTimestampMonotonic > "$stage/service_after.txt"
    cmp "$stage/service_before.txt" "$stage/service_after.txt"
    sha256sum install/tita_controller/lib/tita_controller/tita_node \
        install/tita_controller/lib/tita_controller/run_flashsac.sh \
        "$share/launch/flashsac.launch.py" "$share/launch/tita.launch.py" \
        "$share/policies/$bundle/"* > "$stage/installed.sha256"
    guard_unused_overlay
    echo 'PASS ROBOT_STATE_CHANGING: heading build installed/verified; vendor service unchanged; no motor commands.'
    ;;
*) echo 'Usage: deploy_heading_bundle.sh deploy_build|verify' >&2; exit 2 ;;
esac
