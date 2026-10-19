# p002_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p002_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "gain_velocity": 0.05,
      "gain_tau": 0.6,
      "gain_floor": 0.1
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
  "initial_physics_sha256": "2f491c6051ffa90074a4c339f034d92dbbbe51740597259ac78cca40f029c33d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.027249246219019887,
  "max_drift_m": 0.08937864430389354,
  "radial_IAE_m_s": 2.289972055579968,
  "signed_longitudinal_delta_m": -0.027244335218744215,
  "tail_speed_mean_m_s": 0.00033089840964673433,
  "tail_speed_rms_m_s": 0.0003342804717892464,
  "tail_sensor_speed_mean_m_s": 0.0003391329506469498,
  "tail_fk_speed_mean_m_s": 0.00034295733228281445,
  "peak_tilt_rad": 0.19414184140309287,
  "peak_wheel_torque_nm": 3.325165033340454,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4497377431546678,
  "final_integral_m_s": -0.44978539549924773,
  "elapsed_wall_s": 11.118220993026625
}
```
