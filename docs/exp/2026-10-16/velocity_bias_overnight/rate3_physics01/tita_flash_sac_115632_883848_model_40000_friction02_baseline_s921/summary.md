# tita_flash_sac_115632_883848_model_40000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
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
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "7a0910965132c80beb6b0c6d8f1a93ecc53ff1a27d521ec756660516c6644e3a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.090300977305905,
  "max_drift_m": 6.090300977305905,
  "radial_IAE_m_s": 191.74922524196458,
  "signed_longitudinal_delta_m": 4.414171277193262,
  "tail_speed_mean_m_s": 0.11206434289555088,
  "tail_speed_rms_m_s": 0.11206434291821236,
  "tail_sensor_speed_mean_m_s": 0.11199233923495377,
  "tail_fk_speed_mean_m_s": 0.11200934395609521,
  "peak_tilt_rad": 0.10854514590455921,
  "peak_wheel_torque_nm": 0.21975356340408325,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.845131375011988
}
```
