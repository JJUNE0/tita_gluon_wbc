# tita_flash_sac_115632_883848_model_80000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "f6f9d9ade549d7d505edfab386a7e13cfdd83c9b87888399e31f1214b1a7dc3e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.694953351408381,
  "max_drift_m": 11.694953351408381,
  "radial_IAE_m_s": 345.06414796109743,
  "signed_longitudinal_delta_m": 11.657331683984417,
  "tail_speed_mean_m_s": 0.1995625006541066,
  "tail_speed_rms_m_s": 0.19956277333938258,
  "tail_sensor_speed_mean_m_s": 0.19913142845438403,
  "tail_fk_speed_mean_m_s": 0.19913045771804316,
  "peak_tilt_rad": 0.08728620747184967,
  "peak_wheel_torque_nm": 0.47657912969589233,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.302888214006089
}
```
