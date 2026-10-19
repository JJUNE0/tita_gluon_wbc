# tita_flash_sac_115632_883848_model_40000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "962e7b84f47771bf616f3499d43e7e65fd8e8d1fb58e22760b32e4e6b90e6ac9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.069989068235847,
  "max_drift_m": 8.069989068235847,
  "radial_IAE_m_s": 242.71438767096998,
  "signed_longitudinal_delta_m": 8.043637711988252,
  "tail_speed_mean_m_s": 0.13363930929157725,
  "tail_speed_rms_m_s": 0.1336394623125349,
  "tail_sensor_speed_mean_m_s": 0.133350150192072,
  "tail_fk_speed_mean_m_s": 0.13335063827600882,
  "peak_tilt_rad": 0.11908561045821697,
  "peak_wheel_torque_nm": 0.337354838848114,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.098858083016239
}
```
