"""VALIDATION_SIM: wheel encoders plus IMU only; no root position/velocity."""

from dataclasses import dataclass
import numpy as np
from scipy.spatial.transform import Rotation
from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS


@dataclass
class Sensors:
    joint_position: np.ndarray
    joint_velocity: np.ndarray
    imu_quaternion: np.ndarray  # wxyz
    imu_gyro: np.ndarray       # body frame


class WheelOdometry:
    def __init__(self, description, equilibrium_pitch, wrapped_encoders=False):
        self.description = description
        self.chains = description.wheel_chains()
        self.equilibrium_pitch = equilibrium_pitch
        self.wrapped_encoders = wrapped_encoders
        self.reset()

    def reset(self):
        self.position = 0.
        self.previous = None

    def observe(self, sensors, dt):
        q, dq, quat, gyro = (np.asarray(value, dtype=float) for value in
                             (sensors.joint_position, sensors.joint_velocity,
                              sensors.imu_quaternion, sensors.imu_gyro))
        if q.shape != (8,) or dq.shape != (8,) or quat.shape != (4,) or gyro.shape != (3,):
            raise ValueError('Invalid sensor shapes')
        if not np.isfinite(np.concatenate((q, dq, quat, gyro))).all() or abs(np.linalg.norm(quat)-1) > .01:
            raise ValueError('Invalid sensors')
        rotation = Rotation.from_quat(quat[[1, 2, 3, 0]])
        roll, pitch, yaw = rotation.as_euler('xyz')
        lateral = np.array([-np.sin(yaw), np.cos(yaw), 0.])
        _, axes = self.description.frames(q)
        projections = np.array([lateral @ rotation.apply(axes[name]) for name in NATIVE_JOINTS])
        body_rate = float(lateral @ rotation.apply(gyro))
        rates = [body_rate + sum(projections[i]*dq[i] for i in chain) for chain in self.chains]
        velocity = self.description.radius * np.mean(rates)
        if self.previous is not None:
            prev_q, prev_rotation, prev_projections = self.previous
            delta_q = q - prev_q
            if self.wrapped_encoders:
                delta_q = (delta_q + np.pi) % (2*np.pi) - np.pi
            delta_body = lateral @ (rotation * prev_rotation.inv()).as_rotvec()
            delta = [delta_body + sum((projections[i]+prev_projections[i])/2 * delta_q[i]
                                      for i in chain) for chain in self.chains]
            self.position += self.description.radius * np.mean(delta)
        self.previous = (q.copy(), rotation, projections)
        # Euler pitch derivative, rather than blindly using gyro_y during roll.
        pitch_rate = gyro[1]*np.cos(roll) - gyro[2]*np.sin(roll)
        return np.array([self.position, velocity, pitch-self.equilibrium_pitch, pitch_rate])
