"""TRAINING_SIM: public Experiment1 torque residual environment.

The optional LPF task stays in flat_env_residual_torque_lpf_delay for training.
"""
from .flat_env_residual_torque_sensor_delay import (
    TitaFlatResidualTorqueSensorDelayEnv as TorqueResidualEnv,
    TitaFlatResidualTorqueSensorDelayEnvCfg as TorqueResidualEnvCfg,
)

__all__=['TorqueResidualEnv','TorqueResidualEnvCfg']
