# tita_flash_sac_115632_883848_model_15000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
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
  "initial_physics_sha256": "b836f60d33ed7de7d9e925e2cb424d68fab085070cbfac367cddd0bac789a136",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.682599137796932,
  "max_drift_m": 4.682599137796932,
  "radial_IAE_m_s": 140.91458842157527,
  "signed_longitudinal_delta_m": -4.653346856547949,
  "tail_speed_mean_m_s": -0.07748975742809198,
  "tail_speed_rms_m_s": 0.0795623281853115,
  "tail_sensor_speed_mean_m_s": -0.07696714919866982,
  "tail_fk_speed_mean_m_s": -0.07773212119788268,
  "peak_tilt_rad": 0.11095639830312387,
  "peak_wheel_torque_nm": 5.610372543334961,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.118144568055868
}
```
