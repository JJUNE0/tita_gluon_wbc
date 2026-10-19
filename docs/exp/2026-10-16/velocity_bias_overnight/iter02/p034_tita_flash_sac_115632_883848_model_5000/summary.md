# p034_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p034_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 5.0,
      "ki": 20.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "a14405f43198ecdfbefad595d127e0ed04bbd8d9cfddc7aaa119e9f369851b61",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010332137691349733,
  "max_drift_m": 0.07690497463392182,
  "radial_IAE_m_s": 1.1050429835575797,
  "signed_longitudinal_delta_m": -0.010193996153982678,
  "tail_speed_mean_m_s": 0.0006930576427715559,
  "tail_speed_rms_m_s": 0.0392583038486345,
  "tail_sensor_speed_mean_m_s": 0.0010076535312271236,
  "tail_fk_speed_mean_m_s": 0.0007057203011209696,
  "peak_tilt_rad": 0.1741650079437831,
  "peak_wheel_torque_nm": 4.302055358886719,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2712483150045978,
  "final_integral_m_s": -0.19590026009585754,
  "elapsed_wall_s": 4.729346993030049
}
```
