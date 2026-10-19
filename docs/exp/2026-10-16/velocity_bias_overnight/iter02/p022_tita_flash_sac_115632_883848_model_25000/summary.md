# p022_tita_flash_sac_115632_883848_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p022_tita_flash_sac_115632_883848_model_25000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 2.0,
      "ki": 20.0,
      "tau": 0.2,
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
  "initial_physics_sha256": "0a2be8f2ccd9994fba615ee2737982aba9ec6d63865dd5a06c4954e4fb5a7838",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.24767930953209508,
  "max_drift_m": 0.28361101482042256,
  "radial_IAE_m_s": 13.927643393422597,
  "signed_longitudinal_delta_m": 0.2473587865275964,
  "tail_speed_mean_m_s": 0.00016165533551715892,
  "tail_speed_rms_m_s": 0.04140278906178339,
  "tail_sensor_speed_mean_m_s": 0.00023254794379720187,
  "tail_fk_speed_mean_m_s": 0.0002074180435202856,
  "peak_tilt_rad": 0.14115104873178996,
  "peak_wheel_torque_nm": 1.5799424648284912,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3852607280493985,
  "final_integral_m_s": 1.399384993779611,
  "elapsed_wall_s": 4.805790133017581
}
```
