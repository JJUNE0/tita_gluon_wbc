# tita_flash_sac_115632_883848_model_40000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "1986ebd6d9058fb6a923f3430a8a05bb4029f366ecf28fcfeca6c9f1ce1e5a43",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.030411572127825,
  "max_drift_m": 6.030411572127825,
  "radial_IAE_m_s": 180.4333324715035,
  "signed_longitudinal_delta_m": 6.021039508004148,
  "tail_speed_mean_m_s": 0.10048864536880536,
  "tail_speed_rms_m_s": 0.1004887119016709,
  "tail_sensor_speed_mean_m_s": 0.10027156686320682,
  "tail_fk_speed_mean_m_s": 0.10027138511402779,
  "peak_tilt_rad": 0.11237449388310972,
  "peak_wheel_torque_nm": 0.3011151850223541,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.971580834011547
}
```
