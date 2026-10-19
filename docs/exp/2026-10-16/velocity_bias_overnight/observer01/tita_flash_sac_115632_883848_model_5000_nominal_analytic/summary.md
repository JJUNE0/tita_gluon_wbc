# tita_flash_sac_115632_883848_model_5000_nominal_analytic

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_nominal_analytic",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "analytic",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
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
  "initial_physics_sha256": "40c6cc15c09a62996a0d0a65394972d58e2c12cb9d5933316834715206b8ca86",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04538568152751279,
  "max_drift_m": 0.08803225254125373,
  "radial_IAE_m_s": 2.8557482073616134,
  "signed_longitudinal_delta_m": -0.04537017237965291,
  "tail_speed_mean_m_s": 1.816257392425614e-05,
  "tail_speed_rms_m_s": 2.052878288265322e-05,
  "tail_sensor_speed_mean_m_s": 3.020178094847652e-05,
  "tail_fk_speed_mean_m_s": 3.463750749055748e-05,
  "peak_tilt_rad": 0.17845857290266265,
  "peak_wheel_torque_nm": 4.301686763763428,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4573319078854978,
  "final_integral_m_s": -0.45742227938302,
  "elapsed_wall_s": 16.56843254296109
}
```
