# tita_flash_sac_115632_883848_model_25000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
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
  "initial_physics_sha256": "5a40b7c8376ec83c59a713537e6572d5e2c9491454a451f151ec6a3fa4441570",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.1805653821438915,
  "max_drift_m": 0.2354710935236458,
  "radial_IAE_m_s": 10.641994729799421,
  "signed_longitudinal_delta_m": 0.18055174474724694,
  "tail_speed_mean_m_s": 8.664194447754833e-05,
  "tail_speed_rms_m_s": 8.720761703668671e-05,
  "tail_sensor_speed_mean_m_s": 8.908920941242883e-05,
  "tail_fk_speed_mean_m_s": 0.00010017355922279976,
  "peak_tilt_rad": 0.13060150823207928,
  "peak_wheel_torque_nm": 1.6206121444702148,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3719674954743064,
  "final_integral_m_s": 1.3717957085332333,
  "elapsed_wall_s": 4.445854529971257
}
```
