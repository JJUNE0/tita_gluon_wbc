# Join with TrainingSample by sequence_id AND monotonic_ns in the same recording.
# Separate message preserves the existing TrainingSample wire schema for old bags.
std_msgs/Header header
uint64 sequence_id
uint64 control_tick
uint64 monotonic_ns
string leg_action_filter
# Policy order, before adapter scale/clip and wheel velocity bias. Raw is in TrainingSample.
float32[8] action_applied
