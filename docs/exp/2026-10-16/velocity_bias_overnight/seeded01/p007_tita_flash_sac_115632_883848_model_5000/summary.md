# p007_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p007_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 1.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 4.0
    }
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "final_drift_m": 0.20210871287816798,
  "max_drift_m": 0.20210871287816798,
  "radial_IAE_m_s": 10.923094939969552,
  "signed_longitudinal_delta_m": 0.2020217493462151,
  "tail_speed_mean_m_s": 0.00033137196169222337,
  "tail_speed_rms_m_s": 0.0003358571177326871,
  "tail_sensor_speed_mean_m_s": 0.0003413058929542386,
  "tail_fk_speed_mean_m_s": 0.0003454247198146742,
  "peak_tilt_rad": 0.19817391634218406,
  "peak_wheel_torque_nm": 3.3755621910095215,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.45387822631173574,
  "final_integral_m_s": -0.45387822631173574,
  "elapsed_wall_s": 4.524457610968966
}
```
