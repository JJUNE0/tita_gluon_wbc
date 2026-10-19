# tita_flash_sac_115632_883848_model_25000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "8bf6dc30daf59fef0b3e8f5a0166921d7d163b5727ac83e4d8ae02900bf9765a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08739045192851717,
  "max_drift_m": 0.19740780063517926,
  "radial_IAE_m_s": 4.62693714828594,
  "signed_longitudinal_delta_m": 0.08739044215066105,
  "tail_speed_mean_m_s": 0.00039464083442062307,
  "tail_speed_rms_m_s": 0.00039530375438336107,
  "tail_sensor_speed_mean_m_s": 0.00039525269995378077,
  "tail_fk_speed_mean_m_s": 0.00040422394072756133,
  "peak_tilt_rad": 0.13844146666693402,
  "peak_wheel_torque_nm": 1.289623737335205,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.2673217910496932,
  "final_integral_m_s": 1.2673217910496932,
  "elapsed_wall_s": 11.955673735996243
}
```
