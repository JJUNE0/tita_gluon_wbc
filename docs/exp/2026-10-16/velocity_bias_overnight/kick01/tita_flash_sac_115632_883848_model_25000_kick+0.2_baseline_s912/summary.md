# tita_flash_sac_115632_883848_model_25000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "b90af2a871753ddb5a855a5badacacd32c97c4c02caefafb7aa16ee2f99e65e0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.088116517194287,
  "max_drift_m": 22.088116517194287,
  "radial_IAE_m_s": 669.7676775135616,
  "signed_longitudinal_delta_m": 21.459815217616704,
  "tail_speed_mean_m_s": 0.3736950393967458,
  "tail_speed_rms_m_s": 0.3737043664593062,
  "tail_sensor_speed_mean_m_s": 0.3729081511394254,
  "tail_fk_speed_mean_m_s": 0.3728980088934043,
  "peak_tilt_rad": 0.14800517907025856,
  "peak_wheel_torque_nm": 3.598658561706543,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.737421797995921
}
```
