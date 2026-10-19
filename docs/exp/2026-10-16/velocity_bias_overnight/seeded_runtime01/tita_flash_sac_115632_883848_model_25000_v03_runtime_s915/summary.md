# tita_flash_sac_115632_883848_model_25000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "final_drift_m": 0.09352321975226299,
  "max_drift_m": 0.20868259836329572,
  "radial_IAE_m_s": 5.062509723354842,
  "signed_longitudinal_delta_m": 0.09351998833222087,
  "tail_speed_mean_m_s": 0.0003500042838934454,
  "tail_speed_rms_m_s": 0.0003564488552872115,
  "tail_sensor_speed_mean_m_s": 0.0003483640614025121,
  "tail_fk_speed_mean_m_s": 0.0003576742509342059,
  "peak_tilt_rad": 0.1397804527961639,
  "peak_wheel_torque_nm": 1.5629432201385498,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3444757868565282,
  "final_integral_m_s": 1.3444757868565282,
  "elapsed_wall_s": 13.270581256016158
}
```
