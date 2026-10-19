# tita_flash_sac_115632_883848_model_25000_b+0.00

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_b+0.00",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "0a2be8f2ccd9994fba615ee2737982aba9ec6d63865dd5a06c4954e4fb5a7838",
  "complete": true,
  "failure": [],
  "duration_s": 40.0,
  "final_drift_m": 14.836754366058512,
  "max_drift_m": 14.836754366058512,
  "radial_IAE_m_s": 298.04638471967206,
  "signed_longitudinal_delta_m": 14.543433920273714,
  "tail_speed_mean_m_s": 0.3736985096565374,
  "tail_speed_rms_m_s": 0.3737078438769259,
  "tail_sensor_speed_mean_m_s": 0.37291549275966884,
  "tail_fk_speed_mean_m_s": 0.37290388865756674,
  "peak_tilt_rad": 0.13341002656157896,
  "peak_wheel_torque_nm": 0.6529092788696289,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.6309452070272528
}
```
