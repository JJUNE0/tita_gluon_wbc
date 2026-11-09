"""TRAINING_SIM: shared sensors plus500Hz residual-only LPF before PD sum/delay."""
from dataclasses import dataclass, fields, replace
import math

import torch

from .flat_env_residual_torque_delay import PostPdTorqueDelay, PostPdTorqueDelayCfg
from .flat_env_residual_torque_sensor_delay import (
    TitaFlatResidualTorqueSensorDelayEnv, TitaFlatResidualTorqueSensorDelayEnvCfg,
)
from .flat_env_residual_torque_pose_delay import (
    TitaFlatResidualTorquePoseDelayEnv, TitaFlatResidualTorquePoseDelayEnvCfg,
)


@dataclass(kw_only=True)
class ResidualLpfTorqueDelayCfg(PostPdTorqueDelayCfg):
    residual_lpf_hz: float = 60.

    def __post_init__(self):
        super().__post_init__()
        if not math.isfinite(self.residual_lpf_hz) or not 0 < self.residual_lpf_hz < 250:
            raise ValueError('Residual LPF parameter must lie between0 and250Hz')

    def build(self, entity, target_ids, target_names):
        return ResidualLpfTorqueDelay(self, entity, target_ids, target_names)


class ResidualLpfTorqueDelay(PostPdTorqueDelay):
    def initialize(self, mj_model, model, data, device):
        super().initialize(mj_model, model, data, device)
        dt=float(mj_model.opt.timestep)
        if not math.isclose(dt,.002,abs_tol=1e-10):
            raise ValueError('Residual LPF experiment requires500Hz physics')
        self.residual_lpf_alpha=-math.expm1(-2*math.pi*self.cfg.residual_lpf_hz*dt)
        self.filtered_residual=torch.zeros_like(self.stiffness)

    def compute(self, cmd):
        reset_rows=getattr(self,'_reset_rows',None)
        if reset_rows is not None:
            # A reset forward() is not a physics tick. Never advance another
            # world's filter or torque history during this control write.
            self.filtered_residual[reset_rows]=0.
        else:
            self.filtered_residual.lerp_(cmd.effort_target,self.residual_lpf_alpha)
        # Fresh PD feedback remains untouched. The parent adds/clamps the
        # filtered feedforward term, then applies the episode-fixed delay.
        return super().compute(replace(cmd,effort_target=self.filtered_residual))

    def reset(self, env_ids=None):
        super().reset(env_ids)
        self.filtered_residual[slice(None) if env_ids is None else env_ids]=0.


def _install_filter(cfg, cutoff):
    cfg.residual_lpf_hz=float(cutoff)
    robot=cfg.scene.entities['robot']
    robot.articulation.actuators=tuple(ResidualLpfTorqueDelayCfg(
        **{field.name:getattr(motor,field.name) for field in fields(motor)},
        residual_lpf_hz=cfg.residual_lpf_hz) for motor in robot.articulation.actuators)


def _filter_manifest(value, cutoff):
    value['residual_torque_filter']=dict(kind='one_pole_matched',placement='residual_only',
        cutoff_hz=cutoff,update_hz=500,
        alpha=-math.expm1(-2*math.pi*cutoff*.002),
        reset='zero_on_episode_reset_or_gate_loss',
        actor_previous_residual='requested_pre_filter',
        order='residual LPF -> fresh PD sum -> final effort clamp -> torque delay')
    value['output_semantics']='Requested residual torque in Nm; requires saved500Hz external LPF'
    return value


class TitaFlatResidualTorqueLpfDelayEnvCfg(TitaFlatResidualTorqueSensorDelayEnvCfg):
    def __init__(self, teacher_checkpoint, *, residual_lpf_hz=60., **kwargs):
        if not math.isfinite(residual_lpf_hz) or not 0 < residual_lpf_hz < 250:
            raise ValueError('Residual LPF parameter must lie between0 and250Hz')
        super().__init__(teacher_checkpoint,**kwargs)
        _install_filter(self,residual_lpf_hz)

    def residual_manifest(self):
        return _filter_manifest(super().residual_manifest(),self.residual_lpf_hz)


class TitaFlatResidualTorqueCleanLpfDelayEnvCfg(TitaFlatResidualTorquePoseDelayEnvCfg):
    """Pre-shared-sensor full-pose environment with only residual filtering added."""
    def __init__(self, teacher_checkpoint, *, residual_lpf_hz=60., **kwargs):
        if not math.isfinite(residual_lpf_hz) or not 0 < residual_lpf_hz < 250:
            raise ValueError('Residual LPF parameter must lie between0 and250Hz')
        super().__init__(teacher_checkpoint,**kwargs)
        _install_filter(self,residual_lpf_hz)

    def residual_manifest(self):
        value=super().residual_manifest()
        value.update(actor_sensor_mode='clean',
            teacher_sensor_pipeline='Unchanged saved Teacher noise/bias/delay')
        return _filter_manifest(value,self.residual_lpf_hz)


def _filtered_result(env, result):
    reward,failed,timeout,info=result
    squares=sum(m.filtered_residual.square().sum(1) for m in env.robot.actuators)
    info['filtered_residual_rms_nm']=(squares/env.action_dim).sqrt()
    return reward,failed,timeout,info


class TitaFlatResidualTorqueLpfDelayEnv(TitaFlatResidualTorqueSensorDelayEnv):
    def step(self, residual_nm):
        return _filtered_result(self,super().step(residual_nm))


class TitaFlatResidualTorqueCleanLpfDelayEnv(TitaFlatResidualTorquePoseDelayEnv):
    def step(self, residual_nm):
        return _filtered_result(self,super().step(residual_nm))
