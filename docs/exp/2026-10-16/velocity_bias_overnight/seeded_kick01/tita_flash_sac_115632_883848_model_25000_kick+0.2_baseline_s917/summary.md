# tita_flash_sac_115632_883848_model_25000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "5295976788d620026a502acbf3646d5d6dd247dafd261219331bf4178a743342",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.089675617785062,
  "max_drift_m": 22.089675617785062,
  "radial_IAE_m_s": 669.8095223205521,
  "signed_longitudinal_delta_m": 21.474609927234724,
  "tail_speed_mean_m_s": 0.3736950764276151,
  "tail_speed_rms_m_s": 0.37370440339079397,
  "tail_sensor_speed_mean_m_s": 0.3729082617077369,
  "tail_fk_speed_mean_m_s": 0.3728980392512974,
  "peak_tilt_rad": 0.14790994946619618,
  "peak_wheel_torque_nm": 3.6001243591308594,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.50482508901041
}
```
