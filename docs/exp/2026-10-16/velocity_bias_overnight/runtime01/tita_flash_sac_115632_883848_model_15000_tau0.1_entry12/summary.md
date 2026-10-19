# tita_flash_sac_115632_883848_model_15000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
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
  "initial_physics_sha256": "90341d8253a1eb02abdc274fcacb3ebd28667a54bafbf68c6c81061b3538307b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.034793109965877325,
  "max_drift_m": 0.043638928165003754,
  "radial_IAE_m_s": 2.1097817173851627,
  "signed_longitudinal_delta_m": -0.03474695259111172,
  "tail_speed_mean_m_s": 1.2242476407211827e-05,
  "tail_speed_rms_m_s": 1.3021237018154528e-05,
  "tail_sensor_speed_mean_m_s": 1.246833668639245e-05,
  "tail_fk_speed_mean_m_s": 1.3114022672667297e-05,
  "peak_tilt_rad": 0.12546664515254125,
  "peak_wheel_torque_nm": 2.6044795513153076,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3672448151609416,
  "final_integral_m_s": -0.36725981255892487,
  "elapsed_wall_s": 5.879864251008257
}
```
