# One attempted snapshot per nominal 2 ms motor tick. Sequence gaps indicate
# producer overflow or downstream loss; inspect shutdown counters as well.
# All monotonic timestamps are CONTROLLER times, not CAN RX/acquisition or ACK.
std_msgs/Header header
uint64 sequence_id
uint64 control_tick
uint64 monotonic_ns
uint64 sensor_read_begin_monotonic_ns
uint64 feedback_read_monotonic_ns
uint64 command_begin_monotonic_ns
uint64 command_return_monotonic_ns
uint64 previous_command_monotonic_ns
uint64 capture_dropped_total
float64 loop_interval_us
float64 next_deadline_lateness_us
# 0 idle, 1 damp, 2 transform_up, 3 sit, 4 rl, 5 return_to_sit, 6 estop.
uint8 state
bool sensors_valid
bool feedback_valid
bool policy_valid
bool reference_valid
bool output_enabled
# Successful transport acceptance is not a motor/MCU actuation ACK.
bool torque_sent
bool previous_torque_sent
bool asynchronous_policy
bool residual_result_valid
bool residual_is_action
bool residual_allowed
uint64 policy_worker_sequence
uint64 policy_source_monotonic_ns
uint64 teacher_source_monotonic_ns
# Selected inference timing. Async worker also has its joined PolicyWorkerSample.
uint64 policy_started_monotonic_ns
uint64 policy_completed_monotonic_ns
uint64 policy_epoch
uint64 residual_epoch
# Native joint order throughout, except the two action arrays (policy order).
float64[8] joint_position
float64[8] joint_velocity
# Valid in policy RL only. Position-uncontrolled coordinates (wheels) are NaN.
float64[8] reference_position
float64[8] reference_velocity
float64[8] joint_kp
float64[8] joint_kd
float64[8] effort_limit
float64[8] computed_torque
# Cached SDK-reported Nm, possibly estimated/filtered. Not calibrated truth.
# No receive sequence/timestamp is exposed by this interface. Repeats can be stale.
float64[8] reported_torque
float64[8] previous_computed_torque
float32[8] teacher_action
float32[8] applied_action
# Selected normalized action correction if residual_is_action, Nm otherwise.
float64[8] selected_residual
# Residual-only 500 Hz LPF output before PD sum and final effort clipping.
# A candidate command; torque_sent separately records transport acceptance.
float64[8] filtered_residual
float64 residual_lpf_hz
float64[4] quaternion_wxyz
float64[3] angular_velocity
float64[3] command
float64[3] pose_command
