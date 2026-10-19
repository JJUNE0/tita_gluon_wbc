# p001_tita_flash_sac_115632_883848_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p001_tita_flash_sac_115632_883848_model_25000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": -2.0,
      "ki": 0.5,
      "tau": 0.5,
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
  "final_drift_m": 2.7465888877630773,
  "max_drift_m": 2.7734643716241023,
  "radial_IAE_m_s": 153.7805401836161,
  "signed_longitudinal_delta_m": 2.7461156898817363,
  "tail_speed_mean_m_s": 0.0019169492061583667,
  "tail_speed_rms_m_s": 0.0019322500039965882,
  "tail_sensor_speed_mean_m_s": 0.0019164074367728971,
  "tail_fk_speed_mean_m_s": 0.001927833344188785,
  "peak_tilt_rad": 0.16342579215748398,
  "peak_wheel_torque_nm": 1.7075937986373901,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3699981226469378,
  "final_integral_m_s": 1.3732528040697587,
  "elapsed_wall_s": 5.214833453006577
}
```
