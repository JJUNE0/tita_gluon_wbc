# tita_flash_sac_115632_883848_model_25000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "b90af2a871753ddb5a855a5badacacd32c97c4c02caefafb7aa16ee2f99e65e0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.20537714400142196,
  "max_drift_m": 0.26362380921165823,
  "radial_IAE_m_s": 12.040920133282206,
  "signed_longitudinal_delta_m": 0.2053742368019981,
  "tail_speed_mean_m_s": 0.00014054476348663043,
  "tail_speed_rms_m_s": 0.00014276681980032334,
  "tail_sensor_speed_mean_m_s": 0.00013978600624326118,
  "tail_fk_speed_mean_m_s": 0.00014917935376533272,
  "peak_tilt_rad": 0.14742354593256146,
  "peak_wheel_torque_nm": 3.6678614616394043,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.342322004565634,
  "final_integral_m_s": 1.3421004655321256,
  "elapsed_wall_s": 15.312128661025781
}
```
