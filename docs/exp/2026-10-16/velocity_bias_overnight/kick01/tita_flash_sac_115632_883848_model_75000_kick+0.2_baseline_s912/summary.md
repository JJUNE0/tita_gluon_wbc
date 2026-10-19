# tita_flash_sac_115632_883848_model_75000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "976db50ecf9f15963a0a6fa6dbf1dc065a2548bb9a54cfe6d74271b7b7847419",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.18023723518413645,
  "max_drift_m": 0.18023723518413645,
  "radial_IAE_m_s": 8.959573780491398,
  "signed_longitudinal_delta_m": 0.1802276910685745,
  "tail_speed_mean_m_s": 0.001290529363472748,
  "tail_speed_rms_m_s": 0.0013108890528369845,
  "tail_sensor_speed_mean_m_s": 0.0012878486430680611,
  "tail_fk_speed_mean_m_s": 0.0012883329124540918,
  "peak_tilt_rad": 0.06833466978159963,
  "peak_wheel_torque_nm": 1.7290749549865723,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.778386566962581
}
```
