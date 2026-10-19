# tita_flash_sac_115632_883848_model_5000_b+0.00

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_b+0.00",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
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
  "initial_physics_sha256": "a14405f43198ecdfbefad595d127e0ed04bbd8d9cfddc7aaa119e9f369851b61",
  "complete": true,
  "failure": [],
  "duration_s": 40.0,
  "final_drift_m": 6.757129113545638,
  "max_drift_m": 6.757129113545638,
  "radial_IAE_m_s": 135.82420008232418,
  "signed_longitudinal_delta_m": -6.603567020432005,
  "tail_speed_mean_m_s": -0.16942141246162165,
  "tail_speed_rms_m_s": 0.1706562808243219,
  "tail_sensor_speed_mean_m_s": -0.1688578973910655,
  "tail_fk_speed_mean_m_s": -0.1686201759689337,
  "peak_tilt_rad": 0.07313411326894603,
  "peak_wheel_torque_nm": 3.8889477252960205,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.506903864967171
}
```
