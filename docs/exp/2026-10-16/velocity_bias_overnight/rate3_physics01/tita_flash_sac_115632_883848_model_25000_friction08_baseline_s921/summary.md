# tita_flash_sac_115632_883848_model_25000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "578e8fc3ce4acf04b368d7ae63dbae9a767b4ec4fe82e20378b82a58ebd7e748",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.100465025604546,
  "max_drift_m": 22.100465025604546,
  "radial_IAE_m_s": 668.0358355947069,
  "signed_longitudinal_delta_m": 21.684680278684223,
  "tail_speed_mean_m_s": 0.3735840469316705,
  "tail_speed_rms_m_s": 0.37359321350432473,
  "tail_sensor_speed_mean_m_s": 0.3728062028839083,
  "tail_fk_speed_mean_m_s": 0.3728000035609977,
  "peak_tilt_rad": 0.13925209034178643,
  "peak_wheel_torque_nm": 1.1034443378448486,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.973745736002456
}
```
