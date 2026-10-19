# tita_flash_sac_115632_883848_model_55000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "81c7c835265cf7d4f6eaf6b41183bf337a44c45bd3dc33d5ce6c69b9c86f0977",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007991353167077189,
  "max_drift_m": 0.013124927819031008,
  "radial_IAE_m_s": 0.4964581779629697,
  "signed_longitudinal_delta_m": 0.007974949580270006,
  "tail_speed_mean_m_s": -8.318582076689036e-06,
  "tail_speed_rms_m_s": 8.321220425855434e-06,
  "tail_sensor_speed_mean_m_s": -7.744716355855042e-06,
  "tail_fk_speed_mean_m_s": -6.0034332398265e-06,
  "peak_tilt_rad": 0.10281529884559992,
  "peak_wheel_torque_nm": 0.4667024612426758,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08409655302022048,
  "final_integral_m_s": 0.08410838575503136,
  "elapsed_wall_s": 16.204511146992445
}
```
