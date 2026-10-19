# p003_tita_flash_sac_115632_883848_model_5000_mass13

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p003_tita_flash_sac_115632_883848_model_5000_mass13",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 5.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "ae020d83783585fffe8c24a2a482ecd9ae667912dfb62036eef3182bf7a30336",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.057576238312885226,
  "max_drift_m": 0.05894797531649033,
  "radial_IAE_m_s": 2.6398401781126664,
  "signed_longitudinal_delta_m": -0.05739718452860445,
  "tail_speed_mean_m_s": -0.0005128473870511679,
  "tail_speed_rms_m_s": 0.018370342835939624,
  "tail_sensor_speed_mean_m_s": -0.00035043962669749866,
  "tail_fk_speed_mean_m_s": -5.5364232240239146e-05,
  "peak_tilt_rad": 0.17563914836902494,
  "peak_wheel_torque_nm": 3.6113173961639404,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.16239341998456291,
  "final_integral_m_s": -0.1519001540507377,
  "elapsed_wall_s": 5.68052237998927
}
```
