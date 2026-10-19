# tita_flash_sac_115632_883848_model_65000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "143421bc50f6ba245e2fde4bd43064d990e0844b7a5c2c3e1dc020d91ef7b00c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.9693506188474312,
  "max_drift_m": 1.9693506188474312,
  "radial_IAE_m_s": 60.50591127789271,
  "signed_longitudinal_delta_m": 1.9625963775077884,
  "tail_speed_mean_m_s": 0.031323086256289545,
  "tail_speed_rms_m_s": 0.031326461631479445,
  "tail_sensor_speed_mean_m_s": 0.03125508685675117,
  "tail_fk_speed_mean_m_s": 0.03125398217870196,
  "peak_tilt_rad": 0.059548048478382354,
  "peak_wheel_torque_nm": 0.1960643082857132,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.460651566972956
}
```
