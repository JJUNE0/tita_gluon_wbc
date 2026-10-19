# tita_flash_sac_115632_883848_model_5000_mass1.15_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass1.15_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.15
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "eabd0a1e7b9819644d678457927d21ae39f89eb7b64e52ca3eb9ab77be05334b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.542418947344117,
  "max_drift_m": 4.542418947344117,
  "radial_IAE_m_s": 115.2440931029588,
  "signed_longitudinal_delta_m": -4.497320106077296,
  "tail_speed_mean_m_s": -0.10360986594529863,
  "tail_speed_rms_m_s": 0.10416511905737624,
  "tail_sensor_speed_mean_m_s": -0.10412804048525205,
  "tail_fk_speed_mean_m_s": -0.10344702044573623,
  "peak_tilt_rad": 0.13272906836891263,
  "peak_wheel_torque_nm": 2.7705869674682617,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.994057590025477
}
```
