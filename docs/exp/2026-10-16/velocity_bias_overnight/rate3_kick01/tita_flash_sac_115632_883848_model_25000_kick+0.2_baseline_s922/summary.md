# tita_flash_sac_115632_883848_model_25000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "2db774e34bcd9b401b93659f088930c995b8e04f32720a60d7cd4a95b0925040",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.088116566989015,
  "max_drift_m": 22.088116566989015,
  "radial_IAE_m_s": 669.7676827531845,
  "signed_longitudinal_delta_m": 21.459815998698677,
  "tail_speed_mean_m_s": 0.3736950236967441,
  "tail_speed_rms_m_s": 0.37370435082026315,
  "tail_sensor_speed_mean_m_s": 0.3729081382761135,
  "tail_fk_speed_mean_m_s": 0.37289799357548603,
  "peak_tilt_rad": 0.14800514544718046,
  "peak_wheel_torque_nm": 3.598665475845337,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.125519959023222
}
```
