# tita_flash_sac_193248_068255_model_70000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "37844ec20ef7e72ec50be16c83ce04c85294187e3958769df3b842ee8c41454a",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 18.443225743964867,
  "max_drift_m": 18.443225743964867,
  "radial_IAE_m_s": 2632.3004842650066,
  "signed_longitudinal_delta_m": 18.110800703050785,
  "tail_speed_mean_m_s": 0.06622612120740753,
  "tail_speed_rms_m_s": 0.06622612158457222,
  "tail_sensor_speed_mean_m_s": 0.06608270810028528,
  "tail_fk_speed_mean_m_s": 0.06608167197491217,
  "peak_tilt_rad": 0.08706421104373208,
  "peak_wheel_torque_nm": 0.05625198036432266,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 21.179321818053722
}
```
