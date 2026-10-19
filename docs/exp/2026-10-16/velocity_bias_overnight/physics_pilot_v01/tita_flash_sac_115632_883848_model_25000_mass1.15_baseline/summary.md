# tita_flash_sac_115632_883848_model_25000_mass1.15_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass1.15_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.15
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "46bd649c7b40fa59d68060df35c4502893869b3c26a43512d5815d6e122d82de",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.129450924814735,
  "max_drift_m": 15.129450924814735,
  "radial_IAE_m_s": 455.70088064781976,
  "signed_longitudinal_delta_m": 14.766710244140183,
  "tail_speed_mean_m_s": 0.25467092688234455,
  "tail_speed_rms_m_s": 0.25467982761276026,
  "tail_sensor_speed_mean_m_s": 0.2540945936551467,
  "tail_fk_speed_mean_m_s": 0.2541088804574624,
  "peak_tilt_rad": 0.12930579291361122,
  "peak_wheel_torque_nm": 0.8266483545303345,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.3370630890131
}
```
