# tita_flash_sac_115632_883848_model_25000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "b6fa050ec55bc07791f1fc49df615df85044d4e1931163bf2887f6977ac8f721",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09031812266013202,
  "max_drift_m": 0.1096934404787685,
  "radial_IAE_m_s": 4.703927712966426,
  "signed_longitudinal_delta_m": 0.09031694990367675,
  "tail_speed_mean_m_s": 0.00039758842034812934,
  "tail_speed_rms_m_s": 0.0003995939658346088,
  "tail_sensor_speed_mean_m_s": 0.0003971886505207535,
  "tail_fk_speed_mean_m_s": 0.0004066415328015242,
  "peak_tilt_rad": 0.13100073914072463,
  "peak_wheel_torque_nm": 1.3002992868423462,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3370781041656605,
  "final_integral_m_s": 1.3370781041656605,
  "elapsed_wall_s": 9.715226615022402
}
```
