# tita_flash_sac_115632_883848_model_60000_friction0.8_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction0.8_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "649fa84ed8f31213cbefad3bbd95074ed3eeb15f4ae8ec33d0fbd1e1ffa71dd3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004317442360800952,
  "max_drift_m": 0.006967379273203584,
  "radial_IAE_m_s": 0.2649015522587532,
  "signed_longitudinal_delta_m": 0.004307171990022535,
  "tail_speed_mean_m_s": -9.383016426943417e-06,
  "tail_speed_rms_m_s": 1.0069724485270866e-05,
  "tail_sensor_speed_mean_m_s": -9.525183000050283e-06,
  "tail_fk_speed_mean_m_s": -7.402554508035369e-06,
  "peak_tilt_rad": 0.07035929965112375,
  "peak_wheel_torque_nm": 0.23693910241127014,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0480655033024103,
  "final_integral_m_s": 0.04808481348560836,
  "elapsed_wall_s": 5.3066592129762284
}
```
