# tita_flash_sac_115632_883848_model_45000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "32fd4f89ddbf4dfc2ce3eb6650e73a0175be6673ab84f66b73642cb079f1a5ff",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.703002011647429,
  "max_drift_m": 2.703002011647429,
  "radial_IAE_m_s": 80.20854096749729,
  "signed_longitudinal_delta_m": 2.6223321399894637,
  "tail_speed_mean_m_s": 0.04606124678822225,
  "tail_speed_rms_m_s": 0.0466412864224531,
  "tail_sensor_speed_mean_m_s": 0.046262273627969086,
  "tail_fk_speed_mean_m_s": 0.04608612440419828,
  "peak_tilt_rad": 0.052217929158739684,
  "peak_wheel_torque_nm": 2.6188623905181885,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.428718533017673
}
```
