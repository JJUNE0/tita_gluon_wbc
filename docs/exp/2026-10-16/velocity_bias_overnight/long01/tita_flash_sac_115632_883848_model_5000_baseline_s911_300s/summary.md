# tita_flash_sac_115632_883848_model_5000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "22e4a8f2d12a9dc372fdc0d6564eb78b50a701268c7654595d3f9fc249c2aa35",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 36.05688830726063,
  "max_drift_m": 36.05688830726063,
  "radial_IAE_m_s": 6470.6017962089345,
  "signed_longitudinal_delta_m": -5.057371766004538,
  "tail_speed_mean_m_s": -0.16874787804813673,
  "tail_speed_rms_m_s": 0.16997348384198321,
  "tail_sensor_speed_mean_m_s": -0.16793237013853785,
  "tail_fk_speed_mean_m_s": -0.16789521479855674,
  "peak_tilt_rad": 0.07372194496739759,
  "peak_wheel_torque_nm": 3.892831325531006,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 65.45399370900122
}
```
