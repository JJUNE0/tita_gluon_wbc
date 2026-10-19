# tita_flash_sac_115632_883848_model_25000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "63c6e183e3f88bd83544dd499f0e7e6f50424987acedd45c004963c2a3147373",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 65.8829393235483,
  "max_drift_m": 66.38743798866682,
  "radial_IAE_m_s": 13199.197988051597,
  "signed_longitudinal_delta_m": -0.6844569401804523,
  "tail_speed_mean_m_s": 0.3736956055669211,
  "tail_speed_rms_m_s": 0.3737049321203882,
  "tail_sensor_speed_mean_m_s": 0.3729168202284229,
  "tail_fk_speed_mean_m_s": 0.3728981066015842,
  "peak_tilt_rad": 0.14025172393865248,
  "peak_wheel_torque_nm": 1.143151879310608,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 58.338445016008336
}
```
