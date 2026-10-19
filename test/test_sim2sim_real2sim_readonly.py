"""DESKTOP_DRY_RUN: synthetic state only; no real robot state or commands."""

from pathlib import Path
import sys
import unittest

import numpy as np
import rclpy
from sensor_msgs.msg import Imu, JointState

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.real2sim_node import Real2SimNode
from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS


class ReadOnlyMirrorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init(args=['--ros-args', '-p', 'viewer:=false', '-p', 'real_tita_ns:=synthetic_test_tita'])

    @classmethod
    def tearDownClass(cls):
        rclpy.try_shutdown()

    def setUp(self):
        self.node = Real2SimNode()

    def tearDown(self):
        self.node.env.close()
        self.node.destroy_node()

    def test_joint_names_are_mapped_without_stepping_or_command_publishers(self):
        node = self.node
        node._joints(JointState(name=list(reversed(NATIVE_JOINTS)), position=list(reversed([.1, .8, -1.5, .4]*2)), velocity=list(reversed(list(np.arange(8, dtype=float))))))
        node._step()
        self.assertTrue(node.mapping_ok)
        np.testing.assert_allclose(node.env.joint_pos(), [.1, .8, -1.5, .4]*2)
        np.testing.assert_array_equal(node.env.joint_vel(), np.arange(8))
        self.assertEqual(node.env.data.time, 0.)
        self.assertTrue(all('/command/' not in pub.topic_name and 'cmd_' not in pub.topic_name for pub in node.publishers))

    def test_missing_positions_are_rejected_and_unknown_imu_orientation_is_ignored(self):
        node = self.node
        node._joints(JointState(name=NATIVE_JOINTS, position=[.1]))
        node._update()
        self.assertFalse(node.mapping_ok)
        node._joints(JointState(name=NATIVE_JOINTS, position=[.1, .8, -1.5, 0.]*2))
        imu = Imu()
        imu.orientation.x = 1.
        imu.orientation_covariance[0] = -1.
        node._imu(imu)
        node._update()
        self.assertTrue(node.mapping_ok)
        np.testing.assert_array_equal(node.env.base_quat(), [1., 0., 0., 0.])
        imu.orientation_covariance[0] = 0.
        imu.orientation.x = 0.
        imu.orientation.w = 2.
        node._update()
        np.testing.assert_array_equal(node.env.base_quat(), [1., 0., 0., 0.])


if __name__ == '__main__':
    unittest.main(verbosity=2)
