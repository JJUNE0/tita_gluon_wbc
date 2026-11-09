"""TRAINING_SIM: Experiment2 with residual500Hz, Teacher50Hz, physics/LPF500Hz."""
from .flat_env_residual_torque_lpf_delay import (
    TitaFlatResidualTorqueLpfDelayEnv, TitaFlatResidualTorqueLpfDelayEnvCfg,
)


class TitaFlatResidualTorqueLpf500HzEnvCfg(TitaFlatResidualTorqueLpfDelayEnvCfg):
    def __init__(self, teacher_checkpoint, **kwargs):
        super().__init__(teacher_checkpoint, **kwargs)
        self.decimation = 1

    def residual_manifest(self):
        value = super().residual_manifest()
        value.update(actor_hz=500, history_sample_period_s=.002,
                     history_first_to_last_s=.018,
                     actor_sensor_source='Shared saved Teacher observation noise/bias at500Hz; Teacher consumes same sample at50Hz')
        return value


class TitaFlatResidualTorqueLpf500HzEnv(TitaFlatResidualTorqueLpfDelayEnv):
    dt = .002
    teacher_stride = 10

    def __init__(self, cfg, device='cuda:0'):
        if not isinstance(cfg, TitaFlatResidualTorqueLpf500HzEnvCfg):
            raise TypeError('Residual500Hz requires its saved500Hz config')
        if cfg.decimation != 1 or abs(cfg.sim.mujoco.timestep-.002) > 1e-10:
            raise ValueError('Residual500Hz requires one2ms physics tick per policy step')
        super().__init__(cfg, device)
