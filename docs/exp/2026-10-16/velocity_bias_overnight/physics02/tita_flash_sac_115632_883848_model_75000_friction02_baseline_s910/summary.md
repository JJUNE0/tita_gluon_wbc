# tita_flash_sac_115632_883848_model_75000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "45b5af844095d6fc63ad1423756506b26e2348622680b4ba51f9c442a7c1bec7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.3243689105901546,
  "max_drift_m": 1.3243689105901546,
  "radial_IAE_m_s": 38.70967552664745,
  "signed_longitudinal_delta_m": 1.3240005301913385,
  "tail_speed_mean_m_s": 0.022548702417193308,
  "tail_speed_rms_m_s": 0.022548812873607157,
  "tail_sensor_speed_mean_m_s": 0.02250959839448925,
  "tail_fk_speed_mean_m_s": 0.022510293173167797,
  "peak_tilt_rad": 0.05394098352098187,
  "peak_wheel_torque_nm": 0.1396082490682602,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.557751673040912
}
```
