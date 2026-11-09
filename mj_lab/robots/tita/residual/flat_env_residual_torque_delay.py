"""TRAINING_SIM: episode-fixed 0..8ms delay after PD, residual sum and clamp.

This opt-in task leaves the existing torque/action tasks and shared mjlab backend
unchanged. The command channel carries the complete motor torque at 500Hz.
"""
from dataclasses import dataclass, fields

import torch
from mjlab.actuator.pd_actuator import IdealPdActuator, IdealPdActuatorCfg
from mjlab.utils.buffers import DelayBuffer

from ..common import mdp
from .flat_env_residual_torque import TitaFlatResidualTorqueEnv, TitaFlatResidualTorqueEnvCfg


@dataclass(kw_only=True)
class PostPdTorqueDelayCfg(IdealPdActuatorCfg):
    torque_max_lag: int = 4

    def __post_init__(self):
        super().__post_init__()
        if self.delay_min_lag or self.delay_max_lag:
            raise ValueError('Post-PD delay cannot also delay references')
        if isinstance(self.torque_max_lag, bool) or not isinstance(self.torque_max_lag, int) or self.torque_max_lag < 0:
            raise ValueError('Torque lag must be a nonnegative integer physics-step count')

    def build(self, entity, target_ids, target_names):
        return PostPdTorqueDelay(self, entity, target_ids, target_names)


class PostPdTorqueDelay(IdealPdActuator):
    """Custom compute prevents stateless fusion from bypassing the torque history."""
    def initialize(self, mj_model, model, data, device):
        super().initialize(mj_model, model, data, device)
        self.torque_history = DelayBuffer(min_lag=0, max_lag=self.cfg.torque_max_lag,
                                         batch_size=data.nworld, device=device, hold_prob=1.)
        self.commanded_torque = torch.zeros_like(self.stiffness)
        self.applied_torque = torch.zeros_like(self.stiffness)

    def compute(self, cmd):
        # IdealPd computes fresh feedback + effort and clamps BEFORE storage.
        torque = super().compute(cmd)
        reset_rows = getattr(self, '_reset_rows', None)
        if reset_rows is not None:
            # ManagerBasedRlEnv.reset writes controls for ALL worlds before a
            # forward(), without advancing physics. Only refresh reset rows;
            # do not advance anyone's history or alter the other applied rows.
            self.commanded_torque[reset_rows] = torque[reset_rows]
            self.applied_torque[reset_rows] = torque[reset_rows]
            self._reset_rows = None
            return self.applied_torque
        self.commanded_torque.copy_(torque)
        self.torque_history.append(torque)
        # peek holds the reset-selected lag; no per-tick RNG or lag resampling.
        applied = self.torque_history.peek()
        self.applied_torque.copy_(applied)
        return applied

    def reset(self, env_ids=None):
        super().reset(env_ids)
        self.torque_history.reset(env_ids)
        idx = slice(None) if env_ids is None else env_ids
        self._reset_rows = idx
        self.commanded_torque[idx] = 0.
        self.applied_torque[idx] = 0.


def randomize_post_pd_motors(env, env_ids):
    if env_ids is None:
        env_ids = torch.arange(env.num_envs, device=env.device)
    # Preserve the established gain DR; native set_lags is a no-op because
    # references have no delay buffers in this task.
    mdp.randomize_motors(env, env_ids)
    motors = env.scene['robot'].actuators
    maximum = motors[0].cfg.torque_max_lag
    lags = torch.randint(maximum+1, (len(env_ids),), device=env.device)
    for motor in motors:
        if not isinstance(motor, PostPdTorqueDelay) or motor.cfg.torque_max_lag != maximum:
            raise ValueError('All TITA motors must share the same post-PD lag range')
        motor.torque_history.set_lags(lags, env_ids)


class TitaFlatResidualTorqueDelayEnvCfg(TitaFlatResidualTorqueEnvCfg):
    def __init__(self, teacher_checkpoint, num_envs=4096, episode_length_s=10., seed=42,
                 torque_limit_nm=10., torque_max_lag=4):
        super().__init__(teacher_checkpoint, num_envs=num_envs, episode_length_s=episode_length_s,
                         seed=seed, torque_limit_nm=torque_limit_nm)
        robot = self.scene.entities['robot']
        actuators = []
        for motor in robot.articulation.actuators:
            if type(motor) is not IdealPdActuatorCfg:
                raise ValueError('Post-PD torque task requires saved ideal-PD Teacher motors')
            settings = {field.name: getattr(motor, field.name) for field in fields(motor)}
            settings.update(delay_min_lag=0, delay_max_lag=0)
            actuators.append(PostPdTorqueDelayCfg(**settings, torque_max_lag=torque_max_lag))
        robot.articulation.actuators = tuple(actuators)
        self.torque_max_lag = torque_max_lag
        self.events['randomize_motors'].func = randomize_post_pd_motors

    def residual_manifest(self):
        value = super().residual_manifest()
        value.update(residual_mode='torque', torque_delay_location='after PD+residual sum and final effort clamp',
                     torque_delay_bins_ms=[2*i for i in range(self.torque_max_lag+1)],
                     torque_delay_sampling='Uniform per environment on reset; constant during episode; common to all eight joints',
                     native_reference_delay_ms=0., torque_history_warmup='First valid command / available history, no synthetic zero gap',
                     reset_control_writes='Refresh reset rows only; do not advance torque history without a physics substep',
                     actor_sensor_source='Unchanged existing torque residual proprioceptive frame',
                     output_units='Nm', action_rate_definition='Existing normalized residual torque command difference')
        return value


class TitaFlatResidualTorqueDelayEnv(TitaFlatResidualTorqueEnv):
    def __init__(self, cfg, device='cuda:0'):
        if not isinstance(cfg, TitaFlatResidualTorqueDelayEnvCfg):
            raise TypeError('Use the post-PD torque delay config')
        super().__init__(cfg, device)

    def step(self, residual_nm):
        reward, failed, timeout, info = super().step(residual_nm)
        info['torque_delay_ms'] = self.robot.actuators[0].torque_history.current_lags.float()*2.
        for index, motor in enumerate(self.robot.actuators):
            info[f'torque_channel/{index}_command_rms_nm'] = motor.commanded_torque.square().mean(1).sqrt()
            info[f'torque_channel/{index}_applied_rms_nm'] = motor.applied_torque.square().mean(1).sqrt()
        return reward, failed, timeout, info
