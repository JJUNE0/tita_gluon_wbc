# tita_flash_sac_115632_883848_model_55000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "94343562bb89c26da84ef9dea10c61dddbb9c4449c165be4872ab5197cf08af2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.643113675880463,
  "max_drift_m": 6.643113675880463,
  "radial_IAE_m_s": 196.9583029379171,
  "signed_longitudinal_delta_m": 6.200601873387587,
  "tail_speed_mean_m_s": 0.1130190855158802,
  "tail_speed_rms_m_s": 0.11301909568747844,
  "tail_sensor_speed_mean_m_s": 0.11277702318919122,
  "tail_fk_speed_mean_m_s": 0.11277843983237337,
  "peak_tilt_rad": 0.09068522724566996,
  "peak_wheel_torque_nm": 0.30697101354599,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.8556698760367
}
```
