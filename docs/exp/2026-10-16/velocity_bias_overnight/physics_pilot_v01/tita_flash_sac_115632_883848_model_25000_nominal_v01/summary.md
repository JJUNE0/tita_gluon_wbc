# tita_flash_sac_115632_883848_model_25000_nominal_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_nominal_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
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
  "initial_physics_sha256": "510e82e3500786a169fc86235fd90bfea6c849b554a650600290b4c1fe1749fe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.18056536278354812,
  "max_drift_m": 0.23547112008995608,
  "radial_IAE_m_s": 10.641996962172026,
  "signed_longitudinal_delta_m": 0.180551725690116,
  "tail_speed_mean_m_s": 8.664055586931192e-05,
  "tail_speed_rms_m_s": 8.720656845084288e-05,
  "tail_sensor_speed_mean_m_s": 8.908676222406373e-05,
  "tail_fk_speed_mean_m_s": 0.00010017207480263571,
  "peak_tilt_rad": 0.13060147967293512,
  "peak_wheel_torque_nm": 1.6205809116363525,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.371967067144352,
  "final_integral_m_s": 1.3717950224457498,
  "elapsed_wall_s": 4.768861294025555
}
```
