# tita_flash_sac_115632_883848_model_25000_friction0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: FAIL

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "FAIL",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction0.2_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "84a01faae86299146ddbc589eefbfe1c2819ae0d152720c81fbf0112950a2c58",
  "complete": false,
  "failure": [
    "attitude_limit"
  ],
  "duration_s": 0.98,
  "final_drift_m": 0.005066250610020491,
  "max_drift_m": 0.005066250610020491,
  "radial_IAE_m_s": 0.0020378641975369815,
  "signed_longitudinal_delta_m": 0.005063678178753568,
  "tail_speed_mean_m_s": null,
  "tail_speed_rms_m_s": null,
  "tail_sensor_speed_mean_m_s": null,
  "tail_fk_speed_mean_m_s": null,
  "peak_tilt_rad": 0.6513035767645565,
  "peak_wheel_torque_nm": 5.8820953369140625,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.9163520000000012,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 0.8341286979848519
}
```
