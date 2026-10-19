# Joins TrainingSample by header, sequence_id, control_tick and monotonic_ns.
# Times are controller read times, NOT motor/CAN acquisition times.
std_msgs/Header header
uint64 sequence_id
uint64 control_tick
uint64 monotonic_ns
uint64 feedback_read_monotonic_ns
# SDK motor timeout clear, eight returned values, all finite. Not an actuation ACK.
bool valid
# Native joint order. Firmware-reported Nm, possibly estimated; not calibrated force.
# Invalid reads contain NaN and must be excluded from comparisons.
float64[8] reported_torque
# Most recent preceding 500 Hz command, before this feedback read. Its transport
# result is separate from TrainingSample.torque_sent for the current command.
float64[8] previous_computed_torque
bool previous_torque_sent
# Controller timestamp after the preceding SDK transport call returned (0 if off).
uint64 previous_command_monotonic_ns
