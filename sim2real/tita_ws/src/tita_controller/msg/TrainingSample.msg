# One controller snapshot. Header is ROS time just after sensor read, not CAN acquisition time.
# sequence_id resets on node restart; control_tick counts 2 ms loop iterations.
std_msgs/Header header
uint64 sequence_id
uint64 control_tick
# steady_clock time for interval measurements, independent of ROS/wall clock changes.
uint64 monotonic_ns
string state
bool sensors_valid
# Successful current-frame inference in RL, with no subsequent fault in this tick.
bool policy_valid
bool output_enabled
# CAN transport accepted this tick's command; not a motor acknowledgement.
bool torque_sent
# Teacher target can be inverted through adapter scale/clip. Actor range must also be checked offline.
bool teacher_action_valid
float64[3] command
float32[] observation
# ONNX output units, including export gains; not necessarily normalized [-1, 1].
float32[8] action_raw
float64[2] wheel_velocity_bias
# Equivalent ONNX output for applied (optionally leg-filtered) targets plus wheel bias,
# before PD/effort clipping. Join ActionFilterSample for mode and action_applied.
# Divide by checkpoint export gains when training the normalized actor.
float64[8] teacher_action
# Native joint order for joint/torque fields; action fields retain policy order.
float64[8] computed_torque
float64[8] joint_position
float64[8] joint_velocity
float64[4] quaternion_wxyz
float64[3] angular_velocity
# Same 11-element layout as /sim2real/debug/velocity_bias.
float32[11] velocity_bias_diagnostics
# With asynchronous_policy=true, observation/action originate from PolicyWorkerSample,
# joined by policy_worker_sequence; joint/torque fields remain this motor-loop snapshot.
# policy_valid then means the selected result passed generation/age/fault checks.
bool asynchronous_policy
uint64 policy_worker_sequence
uint64 policy_epoch
uint64 residual_epoch
uint64 policy_source_control_tick
uint64 policy_source_monotonic_ns
uint64 teacher_source_monotonic_ns
float64 policy_result_age_ms
bool residual_result_valid
bool residual_is_action
