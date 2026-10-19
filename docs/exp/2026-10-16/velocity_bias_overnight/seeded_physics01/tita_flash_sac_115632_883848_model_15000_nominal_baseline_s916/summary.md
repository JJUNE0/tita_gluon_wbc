# tita_flash_sac_115632_883848_model_15000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
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
  "initial_physics_sha256": "194ceab6555a3204f7194bd5304c56ad93e7b49be7f7c0559e3131404d1f437d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.637623353991361,
  "max_drift_m": 7.637623353991361,
  "radial_IAE_m_s": 230.38237125684248,
  "signed_longitudinal_delta_m": -7.596669160661479,
  "tail_speed_mean_m_s": -0.12579813650912916,
  "tail_speed_rms_m_s": 0.12580166594912023,
  "tail_sensor_speed_mean_m_s": -0.12556611852681465,
  "tail_fk_speed_mean_m_s": -0.12554876868481105,
  "peak_tilt_rad": 0.058683165632393175,
  "peak_wheel_torque_nm": 1.9245975017547607,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.046207192004658
}
```
