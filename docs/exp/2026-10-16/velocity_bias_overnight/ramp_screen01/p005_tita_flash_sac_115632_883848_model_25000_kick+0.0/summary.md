# p005_tita_flash_sac_115632_883848_model_25000_kick+0.0

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p005_tita_flash_sac_115632_883848_model_25000_kick+0.0",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.1,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "733b4ac62990505761996234d6b7680d713421f07c1b91361c63e66f9f1853d2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09323046124105104,
  "max_drift_m": 0.16654414157728298,
  "radial_IAE_m_s": 4.985414266458395,
  "signed_longitudinal_delta_m": 0.0932300949775814,
  "tail_speed_mean_m_s": 0.00035798374221053547,
  "tail_speed_rms_m_s": 0.0003638928915788637,
  "tail_sensor_speed_mean_m_s": 0.0003565077223346878,
  "tail_fk_speed_mean_m_s": 0.00036583492301083117,
  "peak_tilt_rad": 0.13923447329820027,
  "peak_wheel_torque_nm": 2.141416311264038,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3432180797052464,
  "final_integral_m_s": 1.3432180797052464,
  "elapsed_wall_s": 11.966553860984277
}
```
