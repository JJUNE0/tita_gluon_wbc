# tita_flash_sac_115632_883848_model_5000_mass13_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass13_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "ce4d7c3af5d53de8d905d76ec135dc57b81822f7fe07572693a36359e3d70290",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.5993315273794537,
  "max_drift_m": 2.5993315273794537,
  "radial_IAE_m_s": 77.63404861600134,
  "signed_longitudinal_delta_m": -2.598071166701792,
  "tail_speed_mean_m_s": -0.04372746300955005,
  "tail_speed_rms_m_s": 0.048737261022382905,
  "tail_sensor_speed_mean_m_s": -0.04421917430611055,
  "tail_fk_speed_mean_m_s": -0.04331235538774998,
  "peak_tilt_rad": 0.15233012963572534,
  "peak_wheel_torque_nm": 4.494130611419678,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.678865276044235
}
```
