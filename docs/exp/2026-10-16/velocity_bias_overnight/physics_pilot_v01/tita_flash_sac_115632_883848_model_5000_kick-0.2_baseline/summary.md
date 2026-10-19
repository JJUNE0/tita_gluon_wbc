# tita_flash_sac_115632_883848_model_5000_kick-0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_kick-0.2_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": -0.2,
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
  "initial_physics_sha256": "d222ecc696e8bd0c0400baed13c865b28075d2985658c6708bfb7582915d5def",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.095103100966224,
  "max_drift_m": 10.095103100966224,
  "radial_IAE_m_s": 307.1636700807598,
  "signed_longitudinal_delta_m": -9.624510665664625,
  "tail_speed_mean_m_s": -0.16900100322889222,
  "tail_speed_rms_m_s": 0.17022959725377285,
  "tail_sensor_speed_mean_m_s": -0.16856851674945708,
  "tail_fk_speed_mean_m_s": -0.16818728163804628,
  "peak_tilt_rad": 0.07611338675994128,
  "peak_wheel_torque_nm": 4.396090507507324,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.671581873029936
}
```
