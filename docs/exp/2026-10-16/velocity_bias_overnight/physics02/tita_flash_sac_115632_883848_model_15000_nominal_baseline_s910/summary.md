# tita_flash_sac_115632_883848_model_15000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "be32ccdabba97a03c79b59561f2b8bbccfc1b6eab08ae0d533c09f3193bcbeb3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.478706365667744,
  "max_drift_m": 7.478706365667744,
  "radial_IAE_m_s": 226.939411966266,
  "signed_longitudinal_delta_m": -7.41283797386618,
  "tail_speed_mean_m_s": -0.12225059209744688,
  "tail_speed_rms_m_s": 0.12226080780315282,
  "tail_sensor_speed_mean_m_s": -0.12199633436330753,
  "tail_fk_speed_mean_m_s": -0.12197228256408958,
  "peak_tilt_rad": 0.05863626574748415,
  "peak_wheel_torque_nm": 1.8801110982894897,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.490692388033494
}
```
