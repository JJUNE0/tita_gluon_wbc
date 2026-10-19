# tita_flash_sac_115632_883848_model_15000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "391a9b00e87e65f65a4b372bdebe9ea2cc73a9c5ae6502d07200b094889909f8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.683553351664624,
  "max_drift_m": 7.683553351664624,
  "radial_IAE_m_s": 233.84048903629187,
  "signed_longitudinal_delta_m": -7.639129337963212,
  "tail_speed_mean_m_s": -0.12539329625463136,
  "tail_speed_rms_m_s": 0.12539738229432126,
  "tail_sensor_speed_mean_m_s": -0.12515874178332498,
  "tail_fk_speed_mean_m_s": -0.1251406203241674,
  "peak_tilt_rad": 0.054908423773571746,
  "peak_wheel_torque_nm": 3.864093780517578,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.014633219980169
}
```
