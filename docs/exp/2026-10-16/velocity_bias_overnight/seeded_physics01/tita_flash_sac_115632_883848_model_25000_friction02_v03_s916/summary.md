# tita_flash_sac_115632_883848_model_25000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "7bed7c0abb1e411896bda92e466076863dd5456b59ce101f5d225ee6ad7e573a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08780060399771705,
  "max_drift_m": 0.08796274813145691,
  "radial_IAE_m_s": 2.5064674298354754,
  "signed_longitudinal_delta_m": -0.08771285307587082,
  "tail_speed_mean_m_s": -0.0015061037822160675,
  "tail_speed_rms_m_s": 0.00794801304013957,
  "tail_sensor_speed_mean_m_s": 7.978407931186428,
  "tail_fk_speed_mean_m_s": 7.978361961457321,
  "peak_tilt_rad": 0.6305497787754111,
  "peak_wheel_torque_nm": 6.137836456298828,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.300402127031703
}
```
