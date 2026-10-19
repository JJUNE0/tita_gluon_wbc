# p008_tita_flash_sac_115632_883848_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p008_tita_flash_sac_115632_883848_model_25000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 0.0,
      "ki": 2.0,
      "tau": 0.1,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 1.0,
      "ramp": 1.5
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
  "initial_physics_sha256": "0a2be8f2ccd9994fba615ee2737982aba9ec6d63865dd5a06c4954e4fb5a7838",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.6808446096023392,
  "max_drift_m": 0.6808446096023392,
  "radial_IAE_m_s": 39.09300335418388,
  "signed_longitudinal_delta_m": 0.6808256189455427,
  "tail_speed_mean_m_s": 0.0004935828116326103,
  "tail_speed_rms_m_s": 0.0004949495865011953,
  "tail_sensor_speed_mean_m_s": 0.0004950897477260587,
  "tail_fk_speed_mean_m_s": 0.0005060315982127039,
  "peak_tilt_rad": 0.13187370291390255,
  "peak_wheel_torque_nm": 0.7013992071151733,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3705124866197445,
  "final_integral_m_s": 1.3705124866197445,
  "elapsed_wall_s": 4.790786361030769
}
```
