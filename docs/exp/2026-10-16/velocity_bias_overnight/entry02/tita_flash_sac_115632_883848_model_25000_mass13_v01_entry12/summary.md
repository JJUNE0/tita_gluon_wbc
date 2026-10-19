# tita_flash_sac_115632_883848_model_25000_mass13_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass13_v01_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "9fbc79c4932327d686aca26d9a9ffc7af09003dc2cbf88d8b0bbbc1c7ae32dcb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01778222665313022,
  "max_drift_m": 0.026335676300819608,
  "radial_IAE_m_s": 1.0673503028393143,
  "signed_longitudinal_delta_m": 0.017776873344004174,
  "tail_speed_mean_m_s": 5.071682708202863e-07,
  "tail_speed_rms_m_s": 6.313706519800633e-07,
  "tail_sensor_speed_mean_m_s": 5.362815152733842e-07,
  "tail_fk_speed_mean_m_s": 1.1659991076136025e-06,
  "peak_tilt_rad": 0.11893585611965318,
  "peak_wheel_torque_nm": 1.2776191234588623,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1813825683673508,
  "final_integral_m_s": 0.18138165322039476,
  "elapsed_wall_s": 4.887921999965329
}
```
