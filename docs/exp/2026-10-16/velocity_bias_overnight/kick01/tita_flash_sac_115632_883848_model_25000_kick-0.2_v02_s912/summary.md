# tita_flash_sac_115632_883848_model_25000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "828f3ccee7ebd57ac2d17d31328eb5381f8546d357a2f600f1a5e69e917b1608",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.1273951753428956,
  "max_drift_m": 0.14153546423640298,
  "radial_IAE_m_s": 7.331128873390664,
  "signed_longitudinal_delta_m": 0.12739255988137846,
  "tail_speed_mean_m_s": 0.0001509577650208723,
  "tail_speed_rms_m_s": 0.00015209570509593364,
  "tail_sensor_speed_mean_m_s": 0.00015099469488265944,
  "tail_fk_speed_mean_m_s": 0.0001605022914290577,
  "peak_tilt_rad": 0.1310006334768532,
  "peak_wheel_torque_nm": 1.611331820487976,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.342032521394934,
  "final_integral_m_s": 1.3418065092593638,
  "elapsed_wall_s": 18.92156788497232
}
```
