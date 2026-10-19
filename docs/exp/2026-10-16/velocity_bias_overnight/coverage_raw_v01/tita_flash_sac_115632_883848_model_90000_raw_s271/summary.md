# tita_flash_sac_115632_883848_model_90000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "99ba54f3cf93838ade1079f0b8f6a8ded91d72facbd0f6ddf0df7c69bc5c73d9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.037824764038800765,
  "max_drift_m": 0.05176031374313098,
  "radial_IAE_m_s": 2.2495410262230724,
  "signed_longitudinal_delta_m": 0.0378197523427736,
  "tail_speed_mean_m_s": 3.132323159283661e-05,
  "tail_speed_rms_m_s": 0.005389313249391667,
  "tail_sensor_speed_mean_m_s": 0.0001321932384621599,
  "tail_fk_speed_mean_m_s": 6.480204785889176e-05,
  "peak_tilt_rad": 0.06945421439670452,
  "peak_wheel_torque_nm": 1.2027842998504639,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.28486922586101787,
  "final_integral_m_s": 0.33160326215596886,
  "elapsed_wall_s": 4.4693695940077305
}
```
