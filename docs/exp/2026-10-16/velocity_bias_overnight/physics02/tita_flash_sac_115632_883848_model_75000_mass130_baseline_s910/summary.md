# tita_flash_sac_115632_883848_model_75000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "0b26e4b7a2df55664ac275921ce0b9f6b356b2cb4a25ff2843fb6e2277e92dc4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.949195191371214,
  "max_drift_m": 12.949195191371214,
  "radial_IAE_m_s": 395.135529794098,
  "signed_longitudinal_delta_m": -12.747007165174004,
  "tail_speed_mean_m_s": -0.20916849096786683,
  "tail_speed_rms_m_s": 0.20917655140450542,
  "tail_sensor_speed_mean_m_s": -0.2088045550375376,
  "tail_fk_speed_mean_m_s": -0.20880579894269705,
  "peak_tilt_rad": 0.02373589102589002,
  "peak_wheel_torque_nm": 0.2712061405181885,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.170389150036499
}
```
