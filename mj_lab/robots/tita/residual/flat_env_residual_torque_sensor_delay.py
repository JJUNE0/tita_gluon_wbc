"""TRAINING_SIM: torque residual shares the saved Teacher's noisy sensor samples.

An opt-in variant: actor sensors update at250Hz, Teacher consumes the identical
sample at50Hz. Clean asymmetric critic motion and the existing torque/DR/reward
contracts are retained. Re-reading an observation never samples fresh noise.
"""
import math

import torch

from ..common import mdp
from ..common.robot_cfg import INITIAL_Q, JOINTS, OBS_JOINTS
from .flat_env_residual_torque_pose_delay import (
    TitaFlatResidualTorquePoseDelayEnv, TitaFlatResidualTorquePoseDelayEnvCfg,
)


class TitaFlatResidualTorqueSensorDelayEnvCfg(TitaFlatResidualTorquePoseDelayEnvCfg):
    def residual_manifest(self):
        value = super().residual_manifest()
        group = self.observations['policy']
        value.update(actor_sensor_mode='teacher_shared',
            actor_sensor_source='Shared saved Teacher observation noise/bias at250Hz; Teacher consumes same sample at50Hz',
            actor_sensor_noise_multiplier=1.,
            actor_sensor_noise={name: dict(min=term.noise.n_min, max=term.noise.n_max)
                for name, term in group.terms.items() if term.noise is not None},
            actor_sensor_corruption_enabled=group.enable_corruption,
            actor_sensor_bias_enabled=self.commands['base_velocity'].sensor_bias,
            actor_wheel_error_source='Measured joints/gravity; fixed reference, no velocity latch or input clamp',
            critic_motion_source='Clean simulator state')
        return value


class TitaFlatResidualTorqueSensorDelayEnv(TitaFlatResidualTorquePoseDelayEnv):
    def _initialize_buffers(self):
        super()._initialize_buffers()
        self.shared_observation = torch.zeros(self.n, self.metadata['actor_obs_dim'], device=self.device)
        self.teacher_observation = torch.zeros_like(self.shared_observation)
        self.sensor_age = torch.full_like(self.age, -1)
        self.obs_to_native = torch.tensor([OBS_JOINTS.index(name) for name in JOINTS], device=self.device)
        self.term_slices, self.term_scales = {}, {}
        manager = self.raw.observation_manager
        offset = 0
        for name, shape in zip(manager.active_terms['policy'], manager.group_obs_term_dim['policy']):
            size = math.prod(shape)
            self.term_slices[name] = slice(offset, offset+size)
            scale = manager.get_term_cfg('policy', name).scale
            scale = torch.as_tensor(1. if scale is None else scale, device=self.device, dtype=torch.float32)
            if not bool(torch.isfinite(scale).all()) or bool((scale == 0).any()):
                raise ValueError('Shared sensors require finite nonzero saved scales')
            self.term_scales[name] = torch.broadcast_to(scale, (size,))
            offset += size
        for name, size in dict(base_ang_vel=3, projected_gravity=3, joint_pos=8, joint_vel=8, heading_error=1).items():
            part = self.term_slices.get(name)
            if part is None or part.stop-part.start != size:
                raise ValueError('Saved Teacher sensor layout mismatch: '+name)

    def _capture_observation(self, ids):
        self.shared_observation[ids] = self.raw.obs_buf['policy'][ids]
        self.sensor_age[ids] = self.age[ids]

    def _ensure_sensor_sample(self):
        ids = (self.sensor_age != self.age).nonzero().flatten()
        if len(ids):
            self._capture_observation(ids)

    def _sensor(self, name):
        return self.shared_observation[:, self.term_slices[name]] / self.term_scales[name]

    def measured_joints(self):
        relative = self._sensor('joint_pos')[:, self.obs_to_native]
        q = self.robot.data.default_joint_pos[:, self.ids]+relative
        # Teacher zeroes wheel angle before corruption; restore the encoder
        # signal for residual odometry without dropping its bias/noise.
        command = mdp.velocity(self.raw)
        q[:, [3, 7]] = (self.robot.data.joint_pos[:, self.ids][:, [3, 7]]
            + command.joint_bias[:, self.ids][:, [3, 7]]+relative[:, [3, 7]])
        dq = self._sensor('joint_vel')[:, self.obs_to_native]+self.robot.data.default_joint_vel[:, self.ids]
        return q, dq

    @torch.no_grad()
    def refresh_teacher(self, ids=None):
        self._ensure_sensor_sample()
        if ids is None:
            ids = ((self.age % self.teacher_stride == 0)
                & (self.teacher_updated_at != self.age)).nonzero().flatten()
        if len(ids):
            self.teacher_observation[ids] = self.shared_observation[ids]
            mean, _ = self.teacher.get_mean_and_std(self.teacher_observation[ids], training=False)
            self.teacher_action[ids] = mean.tanh()
            self.teacher_updated_at[ids] = self.age[ids]

    def wheel_angles(self):
        self._ensure_sensor_sample()
        q, _ = self.measured_joints()
        gravity = self._sensor('projected_gravity')
        pitch = torch.atan2(gravity[:, 0], gravity[:, 1:].norm(dim=1))
        return q[:, [3, 7]]+q[:, [1, 5]]+q[:, [2, 6]]+pitch[:, None]

    def residual_error_inputs(self):
        scale = self.raw.observation_manager.get_term_cfg('policy', 'wheel_position_error').scale
        wheel = self.residual_wheel_error if scale is None else self.residual_wheel_error*scale
        return torch.cat((wheel[:, None], self.shared_observation[:, self.term_slices['heading_error']]), 1)

    def frames(self):
        self._ensure_sensor_sample()
        actor, motion = super().frames()
        q, dq = self.measured_joints()
        actor[:, :20] = torch.cat((self._sensor('base_ang_vel')*.25,
            self._sensor('projected_gravity'), (q-q.new_tensor(INITIAL_Q))[:, self.leg_ids]*2.,
            dq*.05), 1).clamp(-10., 10.)
        return actor, motion

    @torch.no_grad()
    def reset_buffers(self, ids):
        self._capture_observation(ids)
        super().reset_buffers(ids)
