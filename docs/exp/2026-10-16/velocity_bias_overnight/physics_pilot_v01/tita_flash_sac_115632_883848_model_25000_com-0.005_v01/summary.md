# tita_flash_sac_115632_883848_model_25000_com-0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com-0.005_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "final_drift_m": 0.16555529352797876,
  "max_drift_m": 0.22666902758065224,
  "radial_IAE_m_s": 9.734363273775564,
  "signed_longitudinal_delta_m": 0.16554368228946836,
  "tail_speed_mean_m_s": 0.00010287598363295507,
  "tail_speed_rms_m_s": 0.00010441482114179393,
  "tail_sensor_speed_mean_m_s": 0.00010453323573069562,
  "tail_fk_speed_mean_m_s": 0.00011522146348043872,
  "peak_tilt_rad": 0.1323711278222559,
  "peak_wheel_torque_nm": 1.2937533855438232,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.310295076253397,
  "final_integral_m_s": 1.3101249196799698,
  "elapsed_wall_s": 5.537954467989039
}
```
