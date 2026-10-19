# tita_flash_sac_115632_883848_model_25000_com-0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com-0.005_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "fd562415f0b52b29219c0f27889be9f845108d4180b55f9b6862269ea0ade837",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 21.295920709220265,
  "max_drift_m": 21.295920709220265,
  "radial_IAE_m_s": 645.6259270484516,
  "signed_longitudinal_delta_m": 20.21183381687125,
  "tail_speed_mean_m_s": 0.36190142238960704,
  "tail_speed_rms_m_s": 0.3619173274731059,
  "tail_sensor_speed_mean_m_s": 0.36121390404262105,
  "tail_fk_speed_mean_m_s": 0.3611377937516821,
  "peak_tilt_rad": 0.13440940197236295,
  "peak_wheel_torque_nm": 0.7261126041412354,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.459213709982578
}
```
