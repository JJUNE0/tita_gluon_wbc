# tita_flash_sac_115632_883848_model_5000_com+0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com+0.005_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "891354843f2232381716947dc4f4176d70fb0dabe09bbbf9ba144f92d7fb858f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.348043444680172,
  "max_drift_m": 9.348043444680172,
  "radial_IAE_m_s": 282.9135657869596,
  "signed_longitudinal_delta_m": -8.941775244184404,
  "tail_speed_mean_m_s": -0.15703306275222095,
  "tail_speed_rms_m_s": 0.15847021623594298,
  "tail_sensor_speed_mean_m_s": -0.15308907626362664,
  "tail_fk_speed_mean_m_s": -0.15613940570960938,
  "peak_tilt_rad": 0.06400732485910088,
  "peak_wheel_torque_nm": 3.798985481262207,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.404002127004787
}
```
