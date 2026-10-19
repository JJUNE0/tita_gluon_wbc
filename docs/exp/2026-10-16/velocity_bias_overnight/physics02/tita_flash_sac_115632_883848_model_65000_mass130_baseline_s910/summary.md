# tita_flash_sac_115632_883848_model_65000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "49e733bdfa30c59dc33a499a66b54190ed988cc3f3d29efd6df268664c2b855a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.741609127349376,
  "max_drift_m": 14.741609127349376,
  "radial_IAE_m_s": 441.56268434575526,
  "signed_longitudinal_delta_m": -14.73140917357671,
  "tail_speed_mean_m_s": -0.24632355033813894,
  "tail_speed_rms_m_s": 0.2463235537866838,
  "tail_sensor_speed_mean_m_s": -0.24579596131960293,
  "tail_fk_speed_mean_m_s": -0.24579499643070357,
  "peak_tilt_rad": 0.03695998081184615,
  "peak_wheel_torque_nm": 0.18562233448028564,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.292348190036137
}
```
