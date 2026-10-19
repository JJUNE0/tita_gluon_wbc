# tita_flash_sac_115632_883848_model_15000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "df2580fb2e7e89a20de9f3866b755d08b2d8321d5e309082c29fd17c387fc840",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.8672299767438,
  "max_drift_m": 7.8672299767438,
  "radial_IAE_m_s": 234.66356965585095,
  "signed_longitudinal_delta_m": -7.85695920530596,
  "tail_speed_mean_m_s": -0.1320141765646325,
  "tail_speed_rms_m_s": 0.13203042918452382,
  "tail_sensor_speed_mean_m_s": -0.13172625029564686,
  "tail_fk_speed_mean_m_s": -0.1317647449610212,
  "peak_tilt_rad": 0.058787901038145796,
  "peak_wheel_torque_nm": 2.017860174179077,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.905016375007108
}
```
