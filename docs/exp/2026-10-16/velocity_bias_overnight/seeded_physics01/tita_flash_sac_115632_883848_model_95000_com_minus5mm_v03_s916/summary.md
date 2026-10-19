# tita_flash_sac_115632_883848_model_95000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "1efa0be7650fb491e06b6fc65ed8a72ede3c3ffa5ab1b641bfc96bb99d4f9fd6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021622349519735174,
  "max_drift_m": 0.021622349519735174,
  "radial_IAE_m_s": 0.9505406634084803,
  "signed_longitudinal_delta_m": 0.021605169737530443,
  "tail_speed_mean_m_s": 0.00019700748326684114,
  "tail_speed_rms_m_s": 0.00019703295528942944,
  "tail_sensor_speed_mean_m_s": 0.00019642537169700875,
  "tail_fk_speed_mean_m_s": 0.00019712296631987976,
  "peak_tilt_rad": 0.06833449064277586,
  "peak_wheel_torque_nm": 0.301120400428772,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.021451440306134575,
  "final_integral_m_s": -0.021451440306134575,
  "elapsed_wall_s": 16.64668626303319
}
```
