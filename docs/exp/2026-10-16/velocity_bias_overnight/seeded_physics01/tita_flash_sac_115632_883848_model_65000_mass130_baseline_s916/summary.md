# tita_flash_sac_115632_883848_model_65000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "d0871b60b28af3961074838e8830503f125937fa14b1a62fc152064a3315da1a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.741607313703303,
  "max_drift_m": 14.741607313703303,
  "radial_IAE_m_s": 441.56260810047274,
  "signed_longitudinal_delta_m": -14.731409122082622,
  "tail_speed_mean_m_s": -0.24632352803109225,
  "tail_speed_rms_m_s": 0.24632353148548736,
  "tail_sensor_speed_mean_m_s": -0.24579594071287908,
  "tail_fk_speed_mean_m_s": -0.24579497480315188,
  "peak_tilt_rad": 0.03695996577726168,
  "peak_wheel_torque_nm": 0.18561804294586182,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.17080242803786
}
```
