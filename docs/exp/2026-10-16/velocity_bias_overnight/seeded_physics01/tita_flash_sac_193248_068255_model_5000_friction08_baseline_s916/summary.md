# tita_flash_sac_193248_068255_model_5000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "4bb46314f84c1b73e05a68fef6eb2c1b8d60bc9aaa199dd53e6d7c43abeaf9d8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.2410468446049314,
  "max_drift_m": 1.5521617500096048,
  "radial_IAE_m_s": 67.10055513975784,
  "signed_longitudinal_delta_m": 0.004827975722854974,
  "tail_speed_mean_m_s": -0.043230906167211244,
  "tail_speed_rms_m_s": 0.04325325833967806,
  "tail_sensor_speed_mean_m_s": -0.04394017107153412,
  "tail_fk_speed_mean_m_s": -0.044346381555568096,
  "peak_tilt_rad": 0.0907006228544025,
  "peak_wheel_torque_nm": 0.7930924892425537,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.452283673977945
}
```
