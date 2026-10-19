#!/usr/bin/env bash
# ROBOT_COMMAND_FREE_RUNTIME: passive CAN receive + ROS subscriptions only.
# No robot SDK constructor, publisher, service mutation, MCU mode or CAN transmit.
set -euo pipefail
set +u
source /opt/ros/humble/setup.bash
source /opt/tita/ros2/setup.bash
set -u
duration=${1:-60}
phase=${2:-stand}
if [[ ! $duration =~ ^[0-9]+$ ]] || (( duration < 10 || duration > 180 )); then
    echo 'ERROR: duration must be an integer from 10 to 180 seconds; capture not started.' >&2
    exit 2
fi
if [[ ! $phase =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$ ]]; then
    echo 'ERROR: label must contain 1-64 letters, digits, _ or -, starting with a letter or digit; capture not started.' >&2
    exit 2
fi
exp=/home/robot/tita_ws/docs/exp/2026-10-18/vendor_baseline_capture
mkdir -p "$exp"
run_id="vendor_${phase}_$(TZ=Asia/Seoul date +%H%M%S_%N)"
summary="$exp/${run_id}_summary.md"
if [[ $(systemctl is-active tita-bringup.service) != active ]]; then
    echo 'Company service is not active; refusing to label this a vendor baseline.' >&2; exit 3
fi
if pgrep -x tita_node >/dev/null; then
    echo 'FlashSAC tita_node is active; refusing vendor baseline capture.' >&2; exit 3
fi
cat > "$summary" <<EOF
# Company baseline, floor standing / operator joystick commands

- Execution Domain: ROBOT_COMMAND_FREE_RUNTIME
- Evidence Status: NOT_TESTED (capture pending; operator movement/load not controlled)
- Policy checkpoint SHA256: N/A (company controller; FlashSAC is not running)
- Comparison FlashSAC checkpoint SHA256: 79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c
- Started: $(TZ=Asia/Seoul date --iso-8601=seconds)
- Operator annotation: normal floor standing, same support condition as previous RL (corrected by operator)
- Phase: $phase; commands, if any, are applied by the operator through the existing joystick
- Requested capture duration: $duration s CAN; ROS recording overlaps and finalizes afterward
- Capture methods: candump -L receive only; ros2 bag record subscriptions only
- Service/MCU/motor output configuration unchanged
- ROS storage contains only actually published topics; absent topics are not fabricated
- Firmware torque telemetry is not calibrated physical torque
EOF
exec > >(tee -a "$exp/${run_id}_capture_console.log") 2>&1
printf 'ROBOT_COMMAND_FREE_RUNTIME RUN_ID=%s\n' "$run_id"
record_pid=
can_pid=
cleanup() {
    code=$?
    trap - EXIT INT TERM
    for pid in "$can_pid" "$record_pid"; do
        if [[ -n $pid ]] && kill -0 "$pid" 2>/dev/null; then
            kill -INT "$pid" 2>/dev/null || true
            for ((i=0;i<30;i++)); do
                if ! kill -0 "$pid" 2>/dev/null; then break; fi
                sleep .1
            done
            if kill -0 "$pid" 2>/dev/null; then kill -TERM "$pid" 2>/dev/null || true; fi
            wait "$pid" 2>/dev/null || true
        fi
    done
    printf '\n- Finished: %s\n- Capture exit: %s\n- Company service after capture: %s\n' \
        "$(TZ=Asia/Seoul date --iso-8601=seconds)" "$code" "$(systemctl is-active tita-bringup.service || true)" >> "$summary"
    echo "ROBOT_COMMAND_FREE_RUNTIME recording complete: $summary (exit $code)"
    exit "$code"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
systemctl show tita-bringup.service -p MainPID -p ActiveState -p SubState > "$exp/${run_id}_service_before.txt"
ros2 topic list -t > "$exp/${run_id}_topics_before.txt"
ros2 node list > "$exp/${run_id}_nodes_before.txt"
env --default-signal=INT,TERM ros2 bag record -o "$exp/${run_id}_bag" \
    /tita4252763/joint_states /tita4252763/imu_sensor_broadcaster/imu \
    /tita4252763/joy /tita4252763/robot_vel /tita4252763/system/status \
    /tita4252763/command/passive/command /tita4252763/command/active/command \
    /tita4252763/chassis/odometry /rosout \
    > "$exp/${run_id}_bag_console.log" 2>&1 &
record_pid=$!
sleep 2
kill -0 "$record_pid"
# Restore the default SIGINT disposition explicitly in the background child.
env --default-signal=INT,TERM candump -L can0 > "$exp/${run_id}_can.log" 2> "$exp/${run_id}_can_stderr.log" &
can_pid=$!
echo "ROBOT_COMMAND_FREE_RUNTIME CAPTURE_READY phase=$phase duration=$duration s"
for ((second=0;second<duration;second++)); do
    sleep 1
    kill -0 "$can_pid"
    kill -0 "$record_pid"
done
systemctl show tita-bringup.service -p MainPID -p ActiveState -p SubState > "$exp/${run_id}_service_after.txt"
printf '\n- Capture runtime: PASS (both receive-only processes alive for $duration s)\n' >> "$summary"
