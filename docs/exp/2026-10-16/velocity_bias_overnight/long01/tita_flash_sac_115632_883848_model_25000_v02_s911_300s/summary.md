# tita_flash_sac_115632_883848_model_25000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "d94b104327c8e147a9de69fb26214cd1864dcbbf974843d65e0950e8bc6829df",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.14691377740472303,
  "max_drift_m": 0.21399331692670007,
  "radial_IAE_m_s": 45.75876745489414,
  "signed_longitudinal_delta_m": 0.14650521879596817,
  "tail_speed_mean_m_s": -9.751796005942982e-05,
  "tail_speed_rms_m_s": 9.763525573482224e-05,
  "tail_sensor_speed_mean_m_s": -0.00010392244795758361,
  "tail_fk_speed_mean_m_s": -8.570647900846696e-05,
  "peak_tilt_rad": 0.13971649434433897,
  "peak_wheel_torque_nm": 1.4569175243377686,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.2684986949119477,
  "final_integral_m_s": 1.268681666859623,
  "elapsed_wall_s": 58.37626780499704
}
```
