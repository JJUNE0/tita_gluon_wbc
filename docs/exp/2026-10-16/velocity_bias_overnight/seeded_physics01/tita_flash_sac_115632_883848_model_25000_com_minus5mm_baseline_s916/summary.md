# tita_flash_sac_115632_883848_model_25000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "8bf6dc30daf59fef0b3e8f5a0166921d7d163b5727ac83e4d8ae02900bf9765a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 21.33003883625275,
  "max_drift_m": 21.33003883625275,
  "radial_IAE_m_s": 645.8343250015996,
  "signed_longitudinal_delta_m": 20.73118857345191,
  "tail_speed_mean_m_s": 0.36190293803415247,
  "tail_speed_rms_m_s": 0.3619188492424887,
  "tail_sensor_speed_mean_m_s": 0.36121915566328766,
  "tail_fk_speed_mean_m_s": 0.36113822152329067,
  "peak_tilt_rad": 0.1387939463306853,
  "peak_wheel_torque_nm": 0.9162588119506836,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.096385748998728
}
```
