# tita_flash_sac_115632_883848_model_25000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "828f3ccee7ebd57ac2d17d31328eb5381f8546d357a2f600f1a5e69e917b1608",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 21.940767294124186,
  "max_drift_m": 21.940767294124186,
  "radial_IAE_m_s": 660.6386672175812,
  "signed_longitudinal_delta_m": 21.325378972683147,
  "tail_speed_mean_m_s": 0.37369596940987726,
  "tail_speed_rms_m_s": 0.3737052966326201,
  "tail_sensor_speed_mean_m_s": 0.37291840579594454,
  "tail_fk_speed_mean_m_s": 0.3728984917160104,
  "peak_tilt_rad": 0.14361879951146017,
  "peak_wheel_torque_nm": 1.9602292776107788,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.99367415800225
}
```
