# tita_flash_sac_115632_883848_model_65000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
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
  "initial_physics_sha256": "0d3896bada0cb7038442ae75fafacb146d8f88e18e776bd464859d825c426985",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 8.493174643350105,
  "max_drift_m": 8.493174643350105,
  "radial_IAE_m_s": 1345.5685404553337,
  "signed_longitudinal_delta_m": 7.813958966470563,
  "tail_speed_mean_m_s": 0.027073272301163926,
  "tail_speed_rms_m_s": 0.027073329498145785,
  "tail_sensor_speed_mean_m_s": 0.027014437669135867,
  "tail_fk_speed_mean_m_s": 0.02701236999685449,
  "peak_tilt_rad": 0.059595743914486965,
  "peak_wheel_torque_nm": 0.2506910562515259,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 46.00774361996446
}
```
