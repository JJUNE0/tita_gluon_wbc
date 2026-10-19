# tita_flash_sac_115632_883848_model_30000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "188e6c9672dfe6187b8b5516fb284d475aa018fd1d540029e291d54aa5654e8e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.101028924534926,
  "max_drift_m": 14.101028924534926,
  "radial_IAE_m_s": 427.8934165054835,
  "signed_longitudinal_delta_m": 14.089410891905446,
  "tail_speed_mean_m_s": 0.23139615184114593,
  "tail_speed_rms_m_s": 0.23139626863800486,
  "tail_sensor_speed_mean_m_s": 0.23089489005438496,
  "tail_fk_speed_mean_m_s": 0.2308933357689082,
  "peak_tilt_rad": 0.1286473295881203,
  "peak_wheel_torque_nm": 0.13434934616088867,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.29020876501454
}
```
