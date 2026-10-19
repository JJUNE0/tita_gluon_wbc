#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: operator-authorized bundle installation/build only.
# ROBOT_COMMAND_FREE_RUNTIME: verification imports launch definitions and runs pure ONNX; no ROS nodes/SDK/CAN.
set -euo pipefail
workspace=/home/robot/tita_ws
stage="$workspace/docs/exp/2026-10-19/sphere_candidates_deployment"
fixtures=test/sim2real/sphere_candidates
bundles=(flashsac_sphere2_60000 flashsac_sphere1_70000 flashsac_sphere1_90000 flashsac_sphere3_70000)
cd "$workspace"
guard_unused_overlay() {
    if pgrep -f '^/home/robot/tita_ws/install/(tita_controller|teleop_command)/lib/' >/dev/null; then
        echo 'Overlay controller/joystick is running; refusing deployment.' >&2
        exit 3
    fi
    # Vendor /opt/tita is a separate installation; leave its service alone.
}
guard_unused_overlay
case ${1:-} in
deploy_build)
    sha256sum -c "$stage/expected_before.sha256"
    sha256sum -c "$stage/payload.sha256"
    for bundle in "${bundles[@]}"; do test ! -e "src/tita_controller/policies/$bundle"; done
    test ! -e "$stage/before_deployment.tar.gz"
    systemctl show tita-bringup.service --property=MainPID --property=ActiveState \
        --property=ExecMainStartTimestampMonotonic > "$stage/service_before.txt"
    sha256sum install/tita_controller/lib/tita_controller/tita_node > "$stage/executable_before.sha256"
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
    cmp src/tita_controller/launch/flashsac.launch.py install/tita_controller/share/tita_controller/launch/flashsac.launch.py
    ort=build/tita_controller/_deps/onnxruntime-src
    g++ -std=c++17 -O2 -I "$ort/include" "$fixtures/inference.cpp" \
        -L "$ort/lib" -Wl,-rpath,"$workspace/$ort/lib" -lonnxruntime -o "$fixtures/inference"
    for bundle in "${bundles[@]}"; do
        for name in policy.onnx config.json manifest.json; do
            cmp "src/tita_controller/policies/$bundle/$name" \
                "install/tita_controller/share/tita_controller/policies/$bundle/$name"
        done
        "$fixtures/inference" "install/tita_controller/share/tita_controller/policies/$bundle/policy.onnx" \
            "$fixtures/$bundle/obs.txt" > "$stage/${bundle}_actual.txt"
    done
    /usr/bin/python3 test/sim2real/verify_sphere_candidates.py install/tita_controller/share/tita_controller \
        "$fixtures" --actual "$stage" --result "$stage/arm_parity.json" | tee "$stage/verify.log"
    ldd install/tita_controller/lib/tita_controller/tita_node > "$stage/linkage.log"
    if grep -q 'not found' "$stage/linkage.log"; then exit 4; fi
    sha256sum -c "$stage/executable_before.sha256"
    systemctl show tita-bringup.service --property=MainPID --property=ActiveState \
        --property=ExecMainStartTimestampMonotonic > "$stage/service_after.txt"
    cmp "$stage/service_before.txt" "$stage/service_after.txt"
    sha256sum install/tita_controller/lib/tita_controller/tita_node \
        install/tita_controller/lib/tita_controller/run_flashsac.sh \
        install/tita_controller/share/tita_controller/launch/flashsac.launch.py > "$stage/installed.sha256"
    for bundle in "${bundles[@]}"; do
        sha256sum "install/tita_controller/share/tita_controller/policies/$bundle/"* >> "$stage/installed.sha256"
    done
    guard_unused_overlay
    echo 'PASS ROBOT_STATE_CHANGING: four bundles built/verified; executable and vendor service PID unchanged; no motor commands.'
    ;;
*) echo 'Usage: deploy_sphere_candidates.sh deploy_build|verify' >&2; exit 2 ;;
esac
