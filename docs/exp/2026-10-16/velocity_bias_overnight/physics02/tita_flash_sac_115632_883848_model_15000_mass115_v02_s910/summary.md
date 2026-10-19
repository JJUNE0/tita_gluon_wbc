# tita_flash_sac_115632_883848_model_15000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
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
  "initial_physics_sha256": "fa774fa5cf2a5fca100792a74723d063525ea287157d4ef9137de6052912910b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02612265266507386,
  "max_drift_m": 0.040764521857843926,
  "radial_IAE_m_s": 2.0081790925612806,
  "signed_longitudinal_delta_m": -0.026022364331171537,
  "tail_speed_mean_m_s": 0.00023841002924645543,
  "tail_speed_rms_m_s": 0.013156160467861654,
  "tail_sensor_speed_mean_m_s": -0.0010672987081610365,
  "tail_fk_speed_mean_m_s": -2.4758248217776075e-05,
  "peak_tilt_rad": 0.14930470221582892,
  "peak_wheel_torque_nm": 5.596818923950195,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.41606767839710757,
  "final_integral_m_s": -0.4022185773573947,
  "elapsed_wall_s": 20.53675511199981
}
```
