# tita_flash_sac_115632_883848_model_15000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "bbcd2cb56e8eba353e5f15cfa2b12619cfcc765a96eddfe2f486275c80131e99",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03329355313651265,
  "max_drift_m": 0.041569828160163025,
  "radial_IAE_m_s": 2.0029938943363996,
  "signed_longitudinal_delta_m": -0.03324702457458288,
  "tail_speed_mean_m_s": 1.1347079702765597e-05,
  "tail_speed_rms_m_s": 1.2209237115255563e-05,
  "tail_sensor_speed_mean_m_s": 1.1588756591857898e-05,
  "tail_fk_speed_mean_m_s": 1.2218571354535048e-05,
  "peak_tilt_rad": 0.12368550892573271,
  "peak_wheel_torque_nm": 3.066133737564087,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3401871191439794,
  "final_integral_m_s": -0.3402022514436539,
  "elapsed_wall_s": 15.613289973989595
}
```
