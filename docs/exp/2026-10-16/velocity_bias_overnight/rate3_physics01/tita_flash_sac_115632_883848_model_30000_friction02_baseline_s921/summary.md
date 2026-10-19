# tita_flash_sac_115632_883848_model_30000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "619a1d2846e8d9a4af4d1cb79ce7d596a907bb81da01786a4837ca8e0ed46dfb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.616538781693148,
  "max_drift_m": 13.616538781693148,
  "radial_IAE_m_s": 407.15587085035753,
  "signed_longitudinal_delta_m": 13.361582756220892,
  "tail_speed_mean_m_s": 0.22983800553354528,
  "tail_speed_rms_m_s": 0.22983806420635752,
  "tail_sensor_speed_mean_m_s": 0.22933025023262063,
  "tail_fk_speed_mean_m_s": 0.22932750178182684,
  "peak_tilt_rad": 0.10761107491097999,
  "peak_wheel_torque_nm": 0.08990240097045898,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.382246371998917
}
```
