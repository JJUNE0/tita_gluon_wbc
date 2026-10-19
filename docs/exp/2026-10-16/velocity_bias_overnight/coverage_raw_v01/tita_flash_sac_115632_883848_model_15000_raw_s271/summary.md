# tita_flash_sac_115632_883848_model_15000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "38e0a9401716ebce5292a6f2350ac667a20398634ad0a3e12b24f9b47662e0b2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03454620072159279,
  "max_drift_m": 0.05147779059574802,
  "radial_IAE_m_s": 2.056021622738762,
  "signed_longitudinal_delta_m": -0.03454606778899271,
  "tail_speed_mean_m_s": -4.53026179645775e-05,
  "tail_speed_rms_m_s": 0.010946679201855741,
  "tail_sensor_speed_mean_m_s": -0.0003949494046449038,
  "tail_fk_speed_mean_m_s": -1.3718311841387195e-05,
  "peak_tilt_rad": 0.1445505938390259,
  "peak_wheel_torque_nm": 1.6029926538467407,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.36021791638983347,
  "final_integral_m_s": -0.40026145322362905,
  "elapsed_wall_s": 4.92280955001479
}
```
