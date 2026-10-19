# tita_flash_sac_115632_883848_model_25000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "b1f147547b4b1231ee5a3b0956689c5ac5a185dc0269dc27cc2edca98f01028c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.5123719575385275,
  "max_drift_m": 5.5123719575385275,
  "radial_IAE_m_s": 165.2131565562749,
  "signed_longitudinal_delta_m": 5.5032716068523,
  "tail_speed_mean_m_s": 0.09193541536820432,
  "tail_speed_rms_m_s": 0.0919354308207965,
  "tail_sensor_speed_mean_m_s": 0.09173793257517435,
  "tail_fk_speed_mean_m_s": 0.09173586467382468,
  "peak_tilt_rad": 0.11973061438453914,
  "peak_wheel_torque_nm": 1.2776029109954834,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.77628339198418
}
```
