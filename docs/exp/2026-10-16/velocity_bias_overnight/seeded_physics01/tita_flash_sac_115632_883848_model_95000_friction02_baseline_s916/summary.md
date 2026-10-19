# tita_flash_sac_115632_883848_model_95000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "375793415f538c2a28ad4a98d64da49b542f61f05947a393d74e42273df2ad4d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.2700597861608753,
  "max_drift_m": 3.2700597861608753,
  "radial_IAE_m_s": 101.95899713274594,
  "signed_longitudinal_delta_m": 2.9676736806886588,
  "tail_speed_mean_m_s": 0.05252338429891214,
  "tail_speed_rms_m_s": 0.05252445509866756,
  "tail_sensor_speed_mean_m_s": 0.05243974967305715,
  "tail_fk_speed_mean_m_s": 0.05244250852042766,
  "peak_tilt_rad": 0.06787880192783335,
  "peak_wheel_torque_nm": 0.24920985102653503,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.512634692015126
}
```
