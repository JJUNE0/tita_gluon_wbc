#!/usr/bin/env bash
# ROBOT_STATE_CHANGING: stop old bringup; controller torque remains off by default.
# Source ROS and this workspace before running. Never restarts robot services.
set -euo pipefail

if [[ $# -gt 1 || ! ${1:-false} =~ ^(false|true)$ ]]; then
    echo "Usage: ./run_flashsac.sh [false|true]  (true enables motor torque)" >&2
    exit 2
fi
output_enabled=${1:-false}
velocity_bias=${TITA_VELOCITY_BIAS:-false}
leg_action_filter=${TITA_LEG_ACTION_FILTER:-auto}
leg_notch_hz=${TITA_LEG_NOTCH_HZ:-8.3}
leg_notch_q=${TITA_LEG_NOTCH_Q:-3.0}
if [[ $leg_action_filter != auto && $leg_action_filter != none && $leg_action_filter != ma2_legs && $leg_action_filter != ma2_notch_legs ]]; then
    echo 'TITA_LEG_ACTION_FILTER must be auto, none, ma2_legs or ma2_notch_legs.' >&2
    exit 2
fi
if [[ -v TITA_VELOCITY_BIAS_MAX_TORQUE ]]; then
    echo 'TITA_VELOCITY_BIAS_MAX_TORQUE is not configurable; additional torque is fixed at +/-0.8 Nm/wheel.' >&2
    exit 2
fi
policy_bundle=${TITA_POLICY_BUNDLE:-flashsac_80000}
case $policy_bundle in
    flashsac_sphere2_60000) policy_checkpoint=a4c2bfbf6a58240a6623ee8bb8d863774b9336f62df7de3d1993b76725334b2a ;;
    flashsac_sphere1_70000) policy_checkpoint=8e23cf5d1844a6d825482939e5cfc455cd672dd566b2320570080ff606782c77 ;;
    flashsac_sphere1_90000) policy_checkpoint=df2a03faeb6e054310c8cc0c2c11f811c1f6e845dd87a66c40ff3cd29dd8b311 ;;
    flashsac_sphere3_70000) policy_checkpoint=b9d411eaee09753d3bb6a00d12da8a3f18ce205b2c95faec954c91699e811263 ;;
    flashsac_posma2_75000) policy_checkpoint=9c22f34e0e3b9d7840f29250c214452bb84cadde6037d277d90df55221e84150 ;;
    flashsac_posma2_50000) policy_checkpoint=baba6974b76d4e8a7b7107cdfab9d2b7bb73695df00419009279549ebd51f992 ;;
    flashsac_80000) policy_checkpoint=79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c ;;
    flashsac_c2_60000) policy_checkpoint=b4c8ae072787c3119864e75c2ebfbaf8284a02976dc68f1f282ad9480ae2e116 ;;
    *) echo "Unknown TITA_POLICY_BUNDLE: $policy_bundle; see flashsac.launch.py policy choices." >&2; exit 2 ;;
esac
velocity_bias_sign=${TITA_VELOCITY_BIAS_RESPONSE_SIGN:-1.0}
if [[ ! $velocity_bias =~ ^(false|true)$ ]]; then
    echo 'TITA_VELOCITY_BIAS must be false or true.' >&2
    exit 2
fi
if [[ ${TITA_INTERNAL_RUNNER:-0} != 1 ]]; then
    exec ros2 launch tita_controller flashsac.launch.py \
        "output_enabled:=$output_enabled" "namespace:=${TITA_NAMESPACE:-tita4252763}" \
        "policy:=$policy_bundle" "velocity_bias:=$velocity_bias" \
        "leg_action_filter:=$leg_action_filter" \
        "leg_notch_hz:=$leg_notch_hz" "leg_notch_q:=$leg_notch_q" \
        "velocity_bias_response_sign:=$velocity_bias_sign"
fi
workspace=${TITA_WORKSPACE:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)}
exp_dir="$workspace/docs/exp/$(TZ=Asia/Seoul date +%F)"
run_id="${policy_bundle}_$(TZ=Asia/Seoul date +%H%M%S_%N)_output_${output_enabled}"
mkdir -p "$exp_dir"
export ROS_LOG_DIR="$exp_dir/ros"
summary="$exp_dir/${run_id}_summary.md"
bag_dir="$exp_dir/${run_id}_bag"
namespace=${TITA_NAMESPACE:-tita4252763}
namespace=${namespace#/}
domain=ROBOT_STATE_CHANGING
cat > "$summary" <<EOF
# Frozen FlashSAC run

- Execution Domain: $domain
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: $(TZ=Asia/Seoul date --iso-8601=seconds)
- Host: $(hostname)
- ROS distribution: ${ROS_DISTRO:-unset}
- Namespace: $namespace
- Output enabled: $output_enabled
- Leg action filter: $leg_action_filter (50 Hz update; wheels pass through; raw last_action)
- Leg notch: $leg_notch_hz Hz, Q $leg_notch_q (active only for ma2_notch_legs; hardware effect NOT_TESTED)
- Velocity bias enabled: $velocity_bias
- Velocity bias limit: additional torque +/-0.8 Nm per wheel (converted using wheel Kd and radius)
- Velocity bias response sign: $velocity_bias_sign (hardware sign NOT_TESTED)
- Velocity bias acquisition: ignore 0-1 s, estimate 1-3 s, correction OFF until 3 s (each neutral hold)
- Velocity bias application: no torque seed; 1 s ramp; correction slew <=0.8 Nm/s per wheel; tracking anti-windup
- Velocity bias posture guard: 5 deg pitch deviation from acquisition mean; latch OFF until command exit/reentry or RL reset
- Supporting sit: 4 s; full leg PD, nominal encoder/IMU CoM wheel balance; software stop latched
- Final torque limits: policy config per-motor effort limits
- Existing service: tita-bringup.service (automatic stop; never automatic restart)
- Policy bundle: $policy_bundle
- Policy checkpoint SHA256: $policy_checkpoint
- Console: ${run_id}_console.log
- Bag: ${run_id}_bag
- Bag console: ${run_id}_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Action filter sample: /sim2real/action_filter_sample (same IDs/time; filter mode and applied action; teacher uses applied targets)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)
EOF
exec > >(tee -i -a "$exp_dir/${run_id}_console.log") 2>&1
echo "[$domain] Logs: $summary"

launch_pid=
bag_pid=
stop_session() {
    local pid=$1
    local label=$2
    echo "[$domain] Stopping owned $label process group $pid."
    # Each child starts its own session. Never signal the shell/operator's group.
    kill -INT -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
    for ((attempt = 0; attempt < 30; ++attempt)); do
        if ! kill -0 -- "-$pid" 2>/dev/null; then break; fi
        sleep .1
    done
    if kill -0 -- "-$pid" 2>/dev/null; then
        echo "[$domain] $label group still present; sending SIGTERM."
        kill -TERM -- "-$pid" 2>/dev/null || true
        for ((attempt = 0; attempt < 20; ++attempt)); do
            if ! kill -0 -- "-$pid" 2>/dev/null; then break; fi
            sleep .1
        done
    fi
    if kill -0 -- "-$pid" 2>/dev/null; then
        echo "[$domain] $label group still present; sending SIGKILL."
        kill -KILL -- "-$pid" 2>/dev/null || true
    fi
    wait "$pid" 2>/dev/null || true
}
cleanup() {
    local result=$?
    trap - EXIT
    # A second Ctrl+C must not abort bounded descendant/recorder cleanup.
    trap '' INT TERM
    if [[ -n $launch_pid ]]; then
        stop_session "$launch_pid" controller
    fi
    if [[ -n $bag_pid ]]; then
        stop_session "$bag_pid" recorder
    fi
    printf '\n- Finished: %s\n- Runner exit code: %s\n' \
        "$(TZ=Asia/Seoul date --iso-8601=seconds)" "$result" >> "$summary"
    echo "[$domain] Exit $result; saved: $summary"
    exit "$result"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

if ! command -v ros2 >/dev/null; then
    echo 'Source /opt/ros/humble/setup.bash and install/setup.bash first.'
    exit 1
fi
prefix=$(ros2 pkg prefix tita_controller)
if [[ $prefix != "$workspace/install/tita_controller" ]]; then
    echo "Wrong tita_controller overlay: $prefix; source this workspace install/setup.bash."
    exit 1
fi
policy_dir="$prefix/share/tita_controller/policies/$policy_bundle"
if [[ $leg_action_filter == auto ]]; then
    leg_action_filter=$(python3 - "$policy_dir/config.json" <<'PYFILTER'
import json
import sys
with open(sys.argv[1]) as stream:
    print(json.load(stream)['policy_interface'].get('leg_action_filter', 'none'))
PYFILTER
    )
    case $leg_action_filter in none|ma2_legs|ma2_notch_legs) ;; *) echo 'Invalid saved action filter.' >&2; exit 2 ;; esac
fi
printf '\n- Resolved leg action filter: %s\n' "$leg_action_filter" >> "$summary"
{
    printf '\n## Installed policy file SHA256\n\n```text\n'
    sha256sum "$policy_dir/policy.onnx" "$policy_dir/config.json"
    printf '```\n'
} >> "$summary"
if [[ $velocity_bias == true ]]; then
    sha256sum "$prefix/share/tita_controller/config/velocity_bias_geometry.json" >> "$summary"
fi
for artifact in "$prefix/lib/tita_controller/tita_node" "$prefix/lib/tita_controller/run_flashsac.sh"; do
    if [[ -f $artifact ]]; then sha256sum "$artifact" >> "$summary"; fi
done

if [[ $output_enabled == true ]] && ! command -v cansend >/dev/null; then
    echo 'cansend is required for the TITA MCU Ready -> Direct request; controller was not started.'
    exit 1
fi

# The public launch already verified the pinned bundle, before any service action.
service=tita-bringup.service
service_state=$(systemctl is-active "$service" || true)
printf '\n- Previous bringup state: %s\n' "$service_state" >> "$summary"
if [[ $service_state != inactive && $service_state != failed && $service_state != unknown ]]; then
    echo "[$domain] Stopping $service (controller output_enabled=$output_enabled)."
    if ! sudo -n /usr/bin/systemctl stop "$service"; then
        echo 'Cannot stop bringup without interactive authentication; no new controller was started.'
        echo 'Authorize this exact systemctl stop command for the operator before launching again.'
        exit 1
    fi
fi
service_state=$(systemctl is-active "$service" || true)
if [[ $service_state != inactive && $service_state != failed && $service_state != unknown ]]; then
    echo "Bringup did not stop (state=$service_state); no new controller was started."
    exit 1
fi
printf '%s\n' '- Bringup after stop: inactive/failed/unknown (not restarted on exit)' >> "$summary"
for ((attempt = 0; attempt < 50; ++attempt)); do
    if ! pgrep -f '(^|/)(ros2_control_node|tita_node|teleop_command_node)( |$)' >/dev/null; then break; fi
    sleep .1
done
if pgrep -f '(^|/)(ros2_control_node|tita_node|teleop_command_node)( |$)' >/dev/null; then
    echo 'Existing motor controller or joystick process detected; refusing concurrent access.'
    pgrep -af '(^|/)(ros2_control_node|tita_node|teleop_command_node)( |$)' || true
    exit 1
fi

# Start recording before the controller and retain explicit topics for later replay.
env --default-signal=INT,TERM setsid --wait ros2 bag record --storage sqlite3 --output "$bag_dir" \
    "/$namespace/joint_states" "/$namespace/imu_sensor_broadcaster/imu" "/$namespace/joy" \
    /sim2real/debug/obs /sim2real/debug/action /sim2real/debug/torque \
    /sim2real/debug/state /sim2real/debug/velocity_bias /sim2real/training_sample /sim2real/motor_feedback /sim2real/action_filter_sample /rosout \
    > "$exp_dir/${run_id}_bag_console.log" 2>&1 &
bag_pid=$!
printf '\n- Recorder process group: %s\n' "$bag_pid" >> "$summary"
ready=false
for ((attempt = 0; attempt < 100; ++attempt)); do
    if ! kill -0 "$bag_pid" 2>/dev/null; then
        echo 'rosbag recorder failed; controller was not started.'
        exit 1
    fi
    if compgen -G "$bag_dir/*.db3" >/dev/null; then ready=true; break; fi
    sleep .1
done
if [[ $ready != true ]]; then
    echo 'rosbag database was not created within 10 s; controller was not started.'
    exit 1
fi

if [[ $output_enabled == true ]]; then
    # Exact upstream ddt_ros2_control/start.bash sequence (SHA256 0a2bca4a146f9127ad558b50ca745826cc93ee920f3bb9538521555ea94f97b3).
    # SDK construction alone does not request Direct mode on the TITA MCU.
    echo "[$domain] Requesting MCU Ready -> Direct before motor controller startup."
    if ! cansend can0 170##200000000000200000000; then
        echo 'MCU Ready request failed; controller was not started.'
        exit 1
    fi
    printf '%s\n' '- MCU Ready request: transport accepted (no independent mode ACK).' >> "$summary"
    sleep .2
    if ! cansend can0 170##200000000000203000000; then
        echo 'MCU Direct request failed; controller was not started.'
        exit 1
    fi
    printf '%s\n' '- MCU Direct request: transport accepted (no independent mode ACK).' >> "$summary"
else
    printf '%s\n' '- MCU mode request: skipped (output disabled).' >> "$summary"
fi

env --default-signal=INT,TERM setsid --wait ros2 launch tita_controller tita.launch.py "policy_dir:=$policy_dir" \
    "output_enabled:=$output_enabled" "namespace:=$namespace" \
    "velocity_bias:=$velocity_bias" \
    "leg_action_filter:=$leg_action_filter" \
    "leg_notch_hz:=$leg_notch_hz" "leg_notch_q:=$leg_notch_q" \
    "velocity_bias_response_sign:=$velocity_bias_sign" &
launch_pid=$!
printf '%s\n' "- Controller process group: $launch_pid" >> "$summary"
while kill -0 "$launch_pid" 2>/dev/null; do
    if ! kill -0 "$bag_pid" 2>/dev/null; then
        echo 'rosbag recorder stopped; stopping controller.'
        exit 1
    fi
    sleep .2
done
wait "$launch_pid"
