# tita_flash_sac_115632_883848_model_15000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
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
  "initial_physics_sha256": "8a46eb8da72f4d8dcedc72e2f3114c61fb96b8817010954a82b7f026409f30c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.965962613001587,
  "max_drift_m": 3.965962613001587,
  "radial_IAE_m_s": 119.57619564803346,
  "signed_longitudinal_delta_m": -3.9412582496297133,
  "tail_speed_mean_m_s": -0.06596915946348751,
  "tail_speed_rms_m_s": 0.0743758899571221,
  "tail_sensor_speed_mean_m_s": -0.06963271890098263,
  "tail_fk_speed_mean_m_s": -0.06656682737770654,
  "peak_tilt_rad": 0.15112073771308432,
  "peak_wheel_torque_nm": 6.851755142211914,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.859603804012295
}
```
