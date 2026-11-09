# Worker input/output association. No field is a CAN acquisition timestamp or motor ACK.
uint64 sequence_id
uint64 epoch
uint64 residual_epoch
uint64 source_control_tick
uint64 source_monotonic_ns
uint64 started_monotonic_ns
uint64 completed_monotonic_ns
uint64 teacher_source_control_tick
uint64 teacher_source_monotonic_ns
bool rl
bool residual_allowed
# requested/previous residual units: normalized [-1,1] if true, Nm otherwise.
bool residual_is_action
bool teacher_updated
bool residual_updated
float64 observation_us
float64 teacher_us
float64 residual_us
float64[8] joint_position
float64[8] joint_velocity
float64[4] quaternion_wxyz
float64[3] angular_velocity
float64[3] command
float64[3] pose_command
# Targets selected by the motor loop when this input snapshot was published.
float32[8] previously_selected_action
float64[8] previously_selected_residual
float32[38] observation
float32[8] teacher_action
float64[8] requested_residual
# Encoder/IMU no-slip body velocity used by the optional residual position latch.
float64[3] latch_velocity_estimate
bool residual_position_latched
float64 residual_wheel_position_error_m
