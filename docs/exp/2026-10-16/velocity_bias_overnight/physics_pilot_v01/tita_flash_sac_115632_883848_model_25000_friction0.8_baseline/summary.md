# tita_flash_sac_115632_883848_model_25000_friction0.8_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction0.8_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "dc08c599e9441da89084a6970ac0c676d9a7ee9485375bc67ee9c0029cfe1390",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.06548771970266,
  "max_drift_m": 22.06548771970266,
  "radial_IAE_m_s": 667.7142195921737,
  "signed_longitudinal_delta_m": 21.188053342397087,
  "tail_speed_mean_m_s": 0.3735836791407627,
  "tail_speed_rms_m_s": 0.3735928441584799,
  "tail_sensor_speed_mean_m_s": 0.37280226134447636,
  "tail_fk_speed_mean_m_s": 0.37279913600739034,
  "peak_tilt_rad": 0.13337628056279227,
  "peak_wheel_torque_nm": 0.6474361419677734,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.36516126600327
}
```
