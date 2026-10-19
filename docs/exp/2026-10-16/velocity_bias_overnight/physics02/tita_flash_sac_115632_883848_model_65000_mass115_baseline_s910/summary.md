# tita_flash_sac_115632_883848_model_65000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "c12475c4b45d12c261f882656e3dcb5d894a98d01453d8dbea41c46bcfec0d98",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.615796770101314,
  "max_drift_m": 8.615796770101314,
  "radial_IAE_m_s": 257.7562441383581,
  "signed_longitudinal_delta_m": -8.56576826874293,
  "tail_speed_mean_m_s": -0.14437261383510674,
  "tail_speed_rms_m_s": 0.1443726140936695,
  "tail_sensor_speed_mean_m_s": -0.14410045286177367,
  "tail_fk_speed_mean_m_s": -0.14410197012064155,
  "peak_tilt_rad": 0.041738517995481006,
  "peak_wheel_torque_nm": 0.22720175981521606,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.270089383004233
}
```
