"""DESKTOP_DRY_RUN: teacher reconstruction and generated-message SQLite round trip.

Source ROS and an overlay containing the new TrainingSample before running.
No controller, hardware API or CAN socket is instantiated.
"""
from pathlib import Path
import math
import subprocess
import tempfile
import unittest

from rclpy.serialization import deserialize_message, serialize_message
import rosbag2_py
from tita_controller.msg import ActionFilterSample, MotorFeedback, TrainingSample

REPO = Path(__file__).resolve().parents[2]


class TrainingLoggingTest(unittest.TestCase):
    def test_filter_sample_join_and_raw_applied_distinction(self):
        sample = TrainingSample()
        sample.sequence_id = 2**53+7
        sample.monotonic_ns = 2**63+20_000_000
        sample.control_tick = 70
        sample.action_raw = [1.]*8
        sample.teacher_action = [.5]*8
        filtered = ActionFilterSample()
        filtered.header = sample.header
        filtered.sequence_id = sample.sequence_id
        filtered.monotonic_ns = sample.monotonic_ns
        filtered.control_tick = sample.control_tick
        filtered.leg_action_filter = 'ma2_legs'
        filtered.action_applied = [.5]*8
        restored = deserialize_message(serialize_message(filtered), ActionFilterSample)
        self.assertEqual(restored, filtered)
        self.assertEqual((restored.sequence_id, restored.monotonic_ns),
                         (sample.sequence_id, sample.monotonic_ns))
        self.assertNotEqual(list(restored.action_applied), list(sample.action_raw))

    def test_feedback_bag_join_keeps_previous_command_and_invalid_reads(self):
        with tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='feedback_bag_') as tmp:
            storage = rosbag2_py.StorageOptions(uri=str(Path(tmp) / 'bag'), storage_id='sqlite3')
            converter = rosbag2_py.ConverterOptions('', '')
            writer = rosbag2_py.SequentialWriter()
            writer.open(storage, converter)
            for i, (topic, name) in enumerate([('/sim2real/training_sample', 'TrainingSample'),
                                               ('/sim2real/motor_feedback', 'MotorFeedback')]):
                fields = dict(name=topic, type='tita_controller/msg/'+name, serialization_format='cdr')
                try:
                    metadata = rosbag2_py.TopicMetadata(id=i, **fields)
                except TypeError:
                    metadata = rosbag2_py.TopicMetadata(**fields)
                writer.create_topic(metadata)
            for i in range(40):
                sample, feedback = TrainingSample(), MotorFeedback()
                sample.header.stamp.sec = 1792200000
                sample.header.stamp.nanosec = i * 20_000_000
                sample.sequence_id = 2**53+i
                sample.control_tick = i*10
                sample.monotonic_ns = 2**63+i*20_000_000
                sample.computed_torque = [float(i+j) for j in range(8)]
                sample.torque_sent = i < 30
                feedback.header = sample.header
                feedback.sequence_id = sample.sequence_id
                feedback.control_tick = sample.control_tick
                feedback.monotonic_ns = sample.monotonic_ns
                feedback.feedback_read_monotonic_ns = sample.monotonic_ns+100_000
                feedback.previous_command_monotonic_ns = sample.monotonic_ns-1_900_000
                feedback.previous_computed_torque = [float(i+j)-.25 for j in range(8)]
                feedback.previous_torque_sent = 0 < i <= 30
                feedback.valid = i != 20
                feedback.reported_torque = ([float(i+j)-.5 for j in range(8)]
                                            if feedback.valid else [float('nan')]*8)
                stamp = sample.header.stamp.sec*10**9+sample.header.stamp.nanosec
                writer.write('/sim2real/training_sample', serialize_message(sample), stamp)
                # Distinct receive times/order still join exactly using integer IDs.
                writer.write('/sim2real/motor_feedback', serialize_message(feedback), stamp+1000)
            del writer
            reader = rosbag2_py.SequentialReader()
            reader.open(storage, converter)
            pairs = {}
            while reader.has_next():
                topic, data, _ = reader.read_next()
                typ = MotorFeedback if topic.endswith('motor_feedback') else TrainingSample
                msg = deserialize_message(data, typ)
                pairs.setdefault(msg.sequence_id, {})[typ.__name__] = msg
            self.assertEqual(len(pairs), 40)
            for index, pair in enumerate(pairs.values()):
                s, f = pair['TrainingSample'], pair['MotorFeedback']
                self.assertEqual(s.header, f.header)
                self.assertEqual(s.control_tick, f.control_tick)
                self.assertEqual(s.monotonic_ns, f.monotonic_ns)
                self.assertLess(f.previous_command_monotonic_ns, s.monotonic_ns)
                self.assertGreater(f.feedback_read_monotonic_ns, s.monotonic_ns)
                self.assertEqual(f.previous_torque_sent, 0 < index <= 30)
                self.assertEqual(list(f.previous_computed_torque), [v-.25 for v in s.computed_torque])
                if index == 20:
                    self.assertFalse(f.valid)
                    self.assertTrue(all(math.isnan(v) for v in f.reported_torque))
                else:
                    self.assertTrue(f.valid)
                    self.assertEqual(list(f.reported_torque), [v-.5 for v in s.computed_torque])
            print('PASS: 40 feedback/training pairs, exact uint64 joins, previous command, NaN/valid flags')

    def test_teacher_matches_corrected_pd_targets(self):
        with tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='teacher_action_') as tmp:
            binary = Path(tmp) / 'runtime'
            subprocess.run([
                'g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
                '-I', str(REPO / 'sim2real/tita_ws/src/tita_controller/include'),
                str(REPO / 'test/sim2real/training_action_runtime.cpp'), '-o', str(binary),
            ], check=True)
            subprocess.run([str(binary)], check=True)

    def test_sqlite_round_trip_preserves_atomic_frames_and_integer_times(self):
        with tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='training_bag_') as tmp:
            storage = rosbag2_py.StorageOptions(uri=str(Path(tmp) / 'bag'), storage_id='sqlite3')
            converter = rosbag2_py.ConverterOptions('', '')
            writer = rosbag2_py.SequentialWriter()
            writer.open(storage, converter)
            topic_fields = dict(name='/sim2real/training_sample',
                                type='tita_controller/msg/TrainingSample', serialization_format='cdr')
            try:
                metadata = rosbag2_py.TopicMetadata(id=0, **topic_fields)  # Jazzy
            except TypeError:
                metadata = rosbag2_py.TopicMetadata(**topic_fields)  # Humble
            writer.create_topic(metadata)
            samples = []
            for i in range(150):
                sample = TrainingSample()
                sample.header.stamp.sec = 1792200000 + i // 50
                sample.header.stamp.nanosec = (i % 50) * 20_000_000
                sample.sequence_id = 2**53 + i
                sample.control_tick = i * 10
                sample.monotonic_ns = 2**63 + i * 20_000_000
                sample.state = 'rl' if i != 75 else 'damp'
                sample.sensors_valid = i != 75
                sample.policy_valid = i != 75
                sample.output_enabled = i < 100
                sample.torque_sent = sample.output_enabled and sample.policy_valid
                sample.teacher_action_valid = sample.policy_valid
                sample.observation = [float(i)] * 33 if sample.sensors_valid else []
                sample.action_raw = [float(i)] * 8
                sample.teacher_action = [float(i) + .125] * 8
                sample.wheel_velocity_bias = [.25, -.5]
                sample.computed_torque = [1., 2., 3., 4., 5., 6., 7., 8.]
                samples.append(sample)
                stamp = sample.header.stamp.sec * 10**9 + sample.header.stamp.nanosec
                writer.write('/sim2real/training_sample', serialize_message(sample), stamp)
            del writer  # Flush/finalize actual SQLite storage before reading it.
            reader = rosbag2_py.SequentialReader()
            reader.open(storage, converter)
            actual = []
            while reader.has_next():
                topic, data, stamp = reader.read_next()
                self.assertEqual(topic, '/sim2real/training_sample')
                sample = deserialize_message(data, TrainingSample)
                self.assertEqual(stamp, sample.header.stamp.sec * 10**9 + sample.header.stamp.nanosec)
                actual.append(sample)
            self.assertEqual(actual, samples)
            self.assertEqual(len(actual), 150)
            self.assertEqual(actual[1].monotonic_ns - actual[0].monotonic_ns, 20_000_000)
            self.assertFalse(actual[75].sensors_valid)
            self.assertEqual(list(actual[75].observation), [])
            self.assertFalse(actual[100].torque_sent)
            print('PASS: 150 atomic SQLite/CDR frames; >2^53 sequence/time precision; '
                  '20 ms intervals, empty/fault frames and output-off flags preserved')


if __name__ == '__main__':
    unittest.main(verbosity=2)
