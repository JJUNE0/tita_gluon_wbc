# tita_flash_sac_115632_883848_model_45000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "619b50f3edd7cabc8780f583b8aa1a261c26604e1c1d5eab25a06e958d46f8e9",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 8.241180005624393,
  "max_drift_m": 8.327324865768444,
  "radial_IAE_m_s": 1627.9098745469723,
  "signed_longitudinal_delta_m": 6.7262784988181155,
  "tail_speed_mean_m_s": -0.008946238034862046,
  "tail_speed_rms_m_s": 0.013739836383059405,
  "tail_sensor_speed_mean_m_s": -0.010274007379004406,
  "tail_fk_speed_mean_m_s": -0.008823689972655875,
  "peak_tilt_rad": 0.05212804219400802,
  "peak_wheel_torque_nm": 4.339997291564941,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 40.87144116702257
}
```
