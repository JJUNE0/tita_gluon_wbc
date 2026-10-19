# tita_flash_sac_115632_883848_model_25000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "6ed7d243899e93f6b73a8dbce623dae284a932d9adc57d95dcb207753de9bb1a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.51237201722099,
  "max_drift_m": 5.51237201722099,
  "radial_IAE_m_s": 165.2131526587898,
  "signed_longitudinal_delta_m": 5.503271679189021,
  "tail_speed_mean_m_s": 0.09193541877262534,
  "tail_speed_rms_m_s": 0.09193543422125255,
  "tail_sensor_speed_mean_m_s": 0.09173793774649336,
  "tail_fk_speed_mean_m_s": 0.09173586829225501,
  "peak_tilt_rad": 0.11973051711769167,
  "peak_wheel_torque_nm": 1.277620792388916,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.10804475704208
}
```
