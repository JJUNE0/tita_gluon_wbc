# tita_flash_sac_115632_883848_model_25000_nominal_fk

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_nominal_fk",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
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
  "initial_physics_sha256": "510e82e3500786a169fc86235fd90bfea6c849b554a650600290b4c1fe1749fe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.18326458048004615,
  "max_drift_m": 0.23855483258556368,
  "radial_IAE_m_s": 10.796652547448296,
  "signed_longitudinal_delta_m": 0.18325031573125636,
  "tail_speed_mean_m_s": 8.653154130219988e-05,
  "tail_speed_rms_m_s": 8.710665586198865e-05,
  "tail_sensor_speed_mean_m_s": 8.898789208405945e-05,
  "tail_fk_speed_mean_m_s": 0.0001000767383219404,
  "peak_tilt_rad": 0.130728039539882,
  "peak_wheel_torque_nm": 1.5894038677215576,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3719985613957617,
  "final_integral_m_s": 1.3718267334529382,
  "elapsed_wall_s": 11.311902059998829
}
```
