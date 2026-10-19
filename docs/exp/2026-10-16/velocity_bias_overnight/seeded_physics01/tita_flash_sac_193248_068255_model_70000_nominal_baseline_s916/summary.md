# tita_flash_sac_193248_068255_model_70000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "442273f22c376e40cbe1a747594a53c21578e7dc9dfbd1e8a64bb20c24c9c1c3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.9450599120450263,
  "max_drift_m": 2.9450599120450263,
  "radial_IAE_m_s": 81.28659845121707,
  "signed_longitudinal_delta_m": 2.9440114605227294,
  "tail_speed_mean_m_s": 0.05625038759282005,
  "tail_speed_rms_m_s": 0.05627135630360499,
  "tail_sensor_speed_mean_m_s": 0.05612930526054404,
  "tail_fk_speed_mean_m_s": 0.05612770870388671,
  "peak_tilt_rad": 0.08404641456286455,
  "peak_wheel_torque_nm": 0.05625171214342117,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.765863484994043
}
```
