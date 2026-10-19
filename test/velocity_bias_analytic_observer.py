"""VALIDATION_SIM: instantaneous FK velocity using only gyro, joints and geometry."""

import numpy as np


def base_forward_speed(data, joints, wheel_bodies, base_body, rotation, dq, gyro, rolling_speed):
    yaw = rotation.as_euler('xyz')[2]
    forward = np.array([np.cos(yaw), np.sin(yaw), 0.])
    omega = rotation.apply(gyro)
    velocities = []
    for side, wheel in enumerate(wheel_bodies):
        indices = np.arange(side * 4, side * 4 + 4)
        ids = joints[indices]
        arm = data.xpos[wheel] - data.xanchor[ids]
        relative = np.sum(np.cross(data.xaxis[ids], arm) * dq[indices, None], axis=0)
        velocities.append(np.cross(omega, data.xpos[wheel] - data.xpos[base_body]) + relative)
    return float(rolling_speed - np.mean(velocities, axis=0) @ forward)
