"""VALIDATION_SIM: startup sequence idle (splay) -> transform_up -> sit -> rl."""

import numpy as np

# Native order: left leg_1..4, right leg_1..4. leg_1 axes are parallel, so mirrored poses flip its sign.
SPLAY_POSE = np.array([0.75, 1.2, -2.7, 0., -0.75, 1.2, -2.7, 0.], dtype=np.float32)
SIT_POSE = np.array([-0.05, 0.9, -2.6, 0., 0.05, 0.9, -2.6, 0.], dtype=np.float32)
# Reference PD from the former cosim transform_up; wheels only get velocity damping.
KP = np.array([600., 80., 80., 0.] * 2, dtype=np.float32)
KD = np.array([8., 8., 8., .5] * 2, dtype=np.float32)
FF = np.array([-20., 0., -25., 0., 20., 0., -25., 0.], dtype=np.float32)
SPLAY_SECONDS_PER_RAD = 4.
SIT_SECONDS = 2.
SETTLE_SECONDS = .2


class StateMachine:
    """idle holds the splay pose; transform_up blends start -> splay -> sit; sit holds; rl runs the policy."""

    def __init__(self, torque_limit, auto_rl=False):
        self.limit = np.asarray(torque_limit, dtype=np.float32)
        self.auto_rl = auto_rl
        self.state, self.target = 'idle', SPLAY_POSE

    def request(self, state, joint_pos):
        """Return False when the request is rejected (rl is only allowed from sit)."""
        if state == 'rl' and self.state != 'sit':
            return False
        if state == 'transform_up':
            self.start, self.elapsed = np.asarray(joint_pos, dtype=np.float32), 0.
        elif state == 'idle':
            self.target = SPLAY_POSE
        self.state = state
        return True

    def update(self, dt):
        if self.state != 'transform_up':
            return
        self.elapsed += dt
        splay_time = max(SPLAY_SECONDS_PER_RAD * float(np.max(np.abs(self.start - SPLAY_POSE))), 1e-6)
        t = self.elapsed
        if t < splay_time:
            self.target = self.start + (SPLAY_POSE - self.start) * (t / splay_time)
        else:
            self.target = SPLAY_POSE + (SIT_POSE - SPLAY_POSE) * min((t - splay_time) / SIT_SECONDS, 1.)
        if t >= splay_time + SIT_SECONDS + SETTLE_SECONDS:
            self.state = 'rl' if self.auto_rl else 'sit'

    def torque(self, joint_pos, joint_vel):
        torque = KP * (self.target - joint_pos) - KD * joint_vel + FF
        return np.clip(torque, -self.limit, self.limit)
