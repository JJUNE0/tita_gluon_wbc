# tita_flash_sac_115632_883848_model_15000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "80c210c3cdf0187476f4a079d64fbe55a4038e6b7f956f4dde4fe411896f29e9",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.033733489508767756,
  "max_drift_m": 0.04363890349491444,
  "radial_IAE_m_s": 10.32158094820006,
  "signed_longitudinal_delta_m": -0.03366615682567476,
  "tail_speed_mean_m_s": 2.8698457635981977e-06,
  "tail_speed_rms_m_s": 2.8721813208675237e-06,
  "tail_sensor_speed_mean_m_s": 3.026471221619614e-06,
  "tail_fk_speed_mean_m_s": 3.255018718745158e-06,
  "peak_tilt_rad": 0.12546662672833397,
  "peak_wheel_torque_nm": 2.6044602394104004,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3547220651976922,
  "final_integral_m_s": -0.35472823675399867,
  "elapsed_wall_s": 88.89733850298217
}
```
