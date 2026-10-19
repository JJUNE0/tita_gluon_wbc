# tita_flash_sac_115632_883848_model_75000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
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
  "initial_physics_sha256": "ac94241e363dfc2576eeb1ad0f2f2fdf115451bad19bcfc57feda238aa6852cc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01949807744467054,
  "max_drift_m": 0.04920956632787767,
  "radial_IAE_m_s": 2.467970110236844,
  "signed_longitudinal_delta_m": -0.01944749204976983,
  "tail_speed_mean_m_s": 0.0010659786932349783,
  "tail_speed_rms_m_s": 0.0010807440476926003,
  "tail_sensor_speed_mean_m_s": 0.0010637813337226836,
  "tail_fk_speed_mean_m_s": 0.0010642801399105486,
  "peak_tilt_rad": 0.05190306978667203,
  "peak_wheel_torque_nm": 0.15775536000728607,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.776894811016973
}
```
