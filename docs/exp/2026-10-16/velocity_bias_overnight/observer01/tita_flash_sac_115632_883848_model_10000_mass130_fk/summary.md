# tita_flash_sac_115632_883848_model_10000_mass130_fk

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass130_fk",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "71af3ba2abad2c7894490b99eec3c868df9493c641cde1bcb329281cb0731f6c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014827011289094274,
  "max_drift_m": 0.016333391431065755,
  "radial_IAE_m_s": 0.8890110577014715,
  "signed_longitudinal_delta_m": -0.014826592887589057,
  "tail_speed_mean_m_s": 2.049829818341725e-05,
  "tail_speed_rms_m_s": 0.004731820732297693,
  "tail_sensor_speed_mean_m_s": 5.710758774749467e-05,
  "tail_fk_speed_mean_m_s": 3.138904924179501e-05,
  "peak_tilt_rad": 0.08626995571289675,
  "peak_wheel_torque_nm": 0.5378716588020325,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.15150134603380447,
  "final_integral_m_s": -0.14702894241805065,
  "elapsed_wall_s": 16.74420336598996
}
```
