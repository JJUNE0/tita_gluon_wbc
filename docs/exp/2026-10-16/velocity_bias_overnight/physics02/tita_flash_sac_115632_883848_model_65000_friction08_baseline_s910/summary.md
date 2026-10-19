# tita_flash_sac_115632_883848_model_65000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "e7d19762292e6b20fdb6e92dee1c7e9e45ad12e0285b240ca4e37346c6e77d6f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.0285159513812445,
  "max_drift_m": 2.0285159513812445,
  "radial_IAE_m_s": 61.7362018551282,
  "signed_longitudinal_delta_m": 2.0100419336577704,
  "tail_speed_mean_m_s": 0.03269475378060193,
  "tail_speed_rms_m_s": 0.032696863444988386,
  "tail_sensor_speed_mean_m_s": 0.03262404040216371,
  "tail_fk_speed_mean_m_s": 0.03262295415658716,
  "peak_tilt_rad": 0.059662398086471,
  "peak_wheel_torque_nm": 0.2304040491580963,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.685713370039593
}
```
