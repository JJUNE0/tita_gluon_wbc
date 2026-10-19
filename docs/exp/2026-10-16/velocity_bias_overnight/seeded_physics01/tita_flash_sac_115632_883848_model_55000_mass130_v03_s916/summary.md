# tita_flash_sac_115632_883848_model_55000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
  "state_columns": [
    "base_x",
    "base_y",
    "base_z",
    "base_forward_speed",
    "roll",
    "pitch",
    "yaw",
    "raw_position",
    "raw_speed",
    "fk_position",
    "fk_speed"
  ],
  "initial_physics_sha256": "653fd6842656906304970fb1902158f0afbc35d5a9808ccab9b4039a24b3fb01",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009268926547536608,
  "max_drift_m": 0.01994225937620093,
  "radial_IAE_m_s": 0.5996155107852211,
  "signed_longitudinal_delta_m": 0.009268075307643748,
  "tail_speed_mean_m_s": -1.8978145143332795e-05,
  "tail_speed_rms_m_s": 1.899524019829176e-05,
  "tail_sensor_speed_mean_m_s": -1.84967412729176e-05,
  "tail_fk_speed_mean_m_s": -1.8061621283206033e-05,
  "peak_tilt_rad": 0.15412758051244135,
  "peak_wheel_torque_nm": 0.7599895596504211,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12767637830462922,
  "final_integral_m_s": -0.12767637830462922,
  "elapsed_wall_s": 13.026635982037988
}
```
