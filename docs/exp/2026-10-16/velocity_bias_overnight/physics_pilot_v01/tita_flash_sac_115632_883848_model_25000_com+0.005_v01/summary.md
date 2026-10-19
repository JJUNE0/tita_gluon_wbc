# tita_flash_sac_115632_883848_model_25000_com+0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com+0.005_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "441c9cf8db4b489410de23d7284edebd9c4ade54d10cbc632a395eceedf777b1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.19641935593634718,
  "max_drift_m": 0.2451232653902696,
  "radial_IAE_m_s": 11.579427981795009,
  "signed_longitudinal_delta_m": 0.1964060447127177,
  "tail_speed_mean_m_s": 8.766621875663547e-05,
  "tail_speed_rms_m_s": 8.818615199378667e-05,
  "tail_sensor_speed_mean_m_s": 9.036872245498432e-05,
  "tail_fk_speed_mean_m_s": 0.0001015778812997683,
  "peak_tilt_rad": 0.12817338270461587,
  "peak_wheel_torque_nm": 1.4968339204788208,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.426366933840817,
  "final_integral_m_s": 1.426172670598155,
  "elapsed_wall_s": 5.477144204021897
}
```
