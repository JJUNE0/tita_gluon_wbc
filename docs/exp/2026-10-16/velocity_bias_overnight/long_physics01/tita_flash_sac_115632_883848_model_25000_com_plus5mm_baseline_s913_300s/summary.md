# tita_flash_sac_115632_883848_model_25000_com_plus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com_plus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "d46689d038f20256223e4b083695967bbe2f8dc063c1f70662593dc6c6068c4c",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 71.68985779420784,
  "max_drift_m": 71.76236158348229,
  "radial_IAE_m_s": 13919.22266860972,
  "signed_longitudinal_delta_m": 4.3707886156382,
  "tail_speed_mean_m_s": 0.38544700566258694,
  "tail_speed_rms_m_s": 0.385447005664981,
  "tail_sensor_speed_mean_m_s": 0.38463911865430145,
  "tail_fk_speed_mean_m_s": 0.38461829853634427,
  "peak_tilt_rad": 0.1412112533648049,
  "peak_wheel_torque_nm": 1.3599770069122314,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 42.34113552601775
}
```
