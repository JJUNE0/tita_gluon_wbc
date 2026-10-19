# tita_flash_sac_115632_883848_model_65000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "2e6e46f5ddca23c3e4a29da43d6d5bb75df7d59539cbddcfdfb3766409b46f45",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.8158003034838923,
  "max_drift_m": 1.8158003034838923,
  "radial_IAE_m_s": 50.98460405038124,
  "signed_longitudinal_delta_m": 1.8069798973145785,
  "tail_speed_mean_m_s": 0.03200883608124474,
  "tail_speed_rms_m_s": 0.032012472071883846,
  "tail_sensor_speed_mean_m_s": 0.03193955745821363,
  "tail_fk_speed_mean_m_s": 0.03193838472109559,
  "peak_tilt_rad": 0.05958184496195562,
  "peak_wheel_torque_nm": 1.5334806442260742,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.037559553980827
}
```
