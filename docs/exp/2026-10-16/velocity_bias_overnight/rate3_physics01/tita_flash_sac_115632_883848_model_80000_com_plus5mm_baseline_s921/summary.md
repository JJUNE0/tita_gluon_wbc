# tita_flash_sac_115632_883848_model_80000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "5a5e57d0e7205214c6c6ffff143a0d4d9a59f22819b72ad6640f1a4ca7dcb0e3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.942588368167895,
  "max_drift_m": 12.942588368167895,
  "radial_IAE_m_s": 382.0861643536103,
  "signed_longitudinal_delta_m": 12.897676019260807,
  "tail_speed_mean_m_s": 0.22056255305648992,
  "tail_speed_rms_m_s": 0.2205627129776595,
  "tail_sensor_speed_mean_m_s": 0.220085950890741,
  "tail_fk_speed_mean_m_s": 0.2200850551546417,
  "peak_tilt_rad": 0.08802805760505139,
  "peak_wheel_torque_nm": 0.5340324640274048,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.160472677031066
}
```
