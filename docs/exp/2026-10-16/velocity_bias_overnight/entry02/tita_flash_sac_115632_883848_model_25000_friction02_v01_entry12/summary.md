# tita_flash_sac_115632_883848_model_25000_friction02_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: FAIL

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "FAIL",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction02_v01_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
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
  "initial_physics_sha256": "935833de9684b3951af9d10f1d663a6bd7a943221f6698776aa91bb0440f9c99",
  "complete": false,
  "failure": [
    "attitude_limit"
  ],
  "duration_s": 0.92,
  "final_drift_m": 0.009419300919422533,
  "max_drift_m": 0.009419300919422533,
  "radial_IAE_m_s": 0.006018761570603203,
  "signed_longitudinal_delta_m": 0.00941804323249798,
  "tail_speed_mean_m_s": null,
  "tail_speed_rms_m_s": null,
  "tail_sensor_speed_mean_m_s": null,
  "tail_fk_speed_mean_m_s": null,
  "peak_tilt_rad": 0.6501723632237866,
  "peak_wheel_torque_nm": 5.663181304931641,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.796352000000001,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 0.32290456496411934
}
```
