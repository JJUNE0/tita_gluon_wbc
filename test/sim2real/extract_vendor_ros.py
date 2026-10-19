"""DESKTOP_DRY_RUN: extract the vendor-controller ROS bags (500 Hz joint_states with effort, IMU, robot_vel).

Read-only on the copied bags under ``docs/exp/2026-10-18/vendor_supported_stand_review``. Writes
``ros_<tag>.npz`` with header-stamped arrays:
- ``imu``: t, quaternion wxyz, gyro xyz, acceleration xyz;
- ``joints``: t, q[8], dq[8], effort[8];
- ``robot_vel``: bag time and value.

Run with the system Python after ``source /opt/ros/jazzy/setup.bash``.
"""

from __future__ import annotations

import argparse
import glob
import sqlite3
from pathlib import Path

import numpy as np
from rclpy.serialization import deserialize_message
from sensor_msgs.msg import Imu, JointState
from std_msgs.msg import Float64

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'docs/exp/2026-10-18/vendor_supported_stand_review'
CAPTURES = {'stand': 'vendor_supported_stand_capture', 'commands': 'vendor_baseline_capture'}


def stamp(m) -> float:
    return m.header.stamp.sec + m.header.stamp.nanosec * 1e-9


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/exp/2026-10-18/vendor_lqr_reproduction')
    parser.add_argument('--captures', type=Path, default=None,
                        help='folder of <run>_bag captures; each becomes ros_<run>.npz (default: the two 11:08 captures)')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.captures:
        jobs = {Path(b).name[:-len('_bag')]: glob.glob(str(Path(b) / '*.db3'))[0]
                for b in sorted(glob.glob(str(args.captures / '*_bag')))}
    else:
        jobs = {tag: glob.glob(str(SOURCE / folder / '*_bag' / '*.db3'))[0] for tag, folder in CAPTURES.items()}
    for tag, db in jobs.items():
        with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
            ids = dict(conn.execute('SELECT name,id FROM topics'))

            def rows(topic, cls):
                return [(ts, deserialize_message(b, cls)) for ts, b in conn.execute(
                    'SELECT timestamp,data FROM messages WHERE topic_id=? ORDER BY timestamp', (ids[topic],))]
            imu = rows('/tita4252763/imu_sensor_broadcaster/imu', Imu)
            joints = rows('/tita4252763/joint_states', JointState)
            vel = rows('/tita4252763/robot_vel', Float64)
        i = np.array([[stamp(m), m.orientation.w, m.orientation.x, m.orientation.y, m.orientation.z,
                       m.angular_velocity.x, m.angular_velocity.y, m.angular_velocity.z,
                       m.linear_acceleration.x, m.linear_acceleration.y, m.linear_acceleration.z] for _, m in imu])
        j = np.array([[stamp(m), *m.position, *m.velocity, *m.effort] for _, m in joints if len(m.effort) == 8])
        v = np.array([[ts * 1e-9, m.data] for ts, m in vel])
        np.savez_compressed(args.output / f'ros_{tag}.npz', imu=i, joints=j, robot_vel=v, db=db)
        print(f'[DESKTOP_DRY_RUN] {tag}: imu {len(i)}, joints {len(j)}, robot_vel {len(v)} from {db}')


if __name__ == '__main__':
    main()
