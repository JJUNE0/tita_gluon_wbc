# tita_flash_sac_115632_883848_model_75000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "da33d50d8949321e481289deb3a432a2dc43a47334e2fa4a796f25a5571d42d5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.18023717137892376,
  "max_drift_m": 0.18023717137892376,
  "radial_IAE_m_s": 8.959574614707336,
  "signed_longitudinal_delta_m": 0.1802276272764844,
  "tail_speed_mean_m_s": 0.0012905246687510221,
  "tail_speed_rms_m_s": 0.0013108840550292609,
  "tail_sensor_speed_mean_m_s": 0.001287844656506681,
  "tail_fk_speed_mean_m_s": 0.001288328509802346,
  "peak_tilt_rad": 0.06833466644019093,
  "peak_wheel_torque_nm": 1.7290775775909424,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.451835488027427
}
```
