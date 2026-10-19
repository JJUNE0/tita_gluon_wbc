# tita_flash_sac_115632_883848_model_40000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "edb5fa1c5d57c2673b764fb3ebea1e7a6994ba2538784f9025493ac3e1c42d07",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.030411813972019,
  "max_drift_m": 6.030411813972019,
  "radial_IAE_m_s": 180.43334722847695,
  "signed_longitudinal_delta_m": 6.021039751022988,
  "tail_speed_mean_m_s": 0.1004886449966113,
  "tail_speed_rms_m_s": 0.10048871155785508,
  "tail_sensor_speed_mean_m_s": 0.10027156836963419,
  "tail_fk_speed_mean_m_s": 0.10027138470352913,
  "peak_tilt_rad": 0.11237449185993498,
  "peak_wheel_torque_nm": 0.3011038899421692,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.76940178294899
}
```
