# p011_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p011_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 15.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 4.0
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
  "final_drift_m": 0.014773074761233854,
  "max_drift_m": 0.09598541190206451,
  "radial_IAE_m_s": 1.8058917784023483,
  "signed_longitudinal_delta_m": 0.013899194142956933,
  "tail_speed_mean_m_s": 0.0013996373609528206,
  "tail_speed_rms_m_s": 0.06652112182833242,
  "tail_sensor_speed_mean_m_s": 0.0010405083740777441,
  "tail_fk_speed_mean_m_s": 0.0015151513697568189,
  "peak_tilt_rad": 0.2029119992272641,
  "peak_wheel_torque_nm": 3.4407706260681152,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.45664142593538337,
  "final_integral_m_s": 0.16716292293102433,
  "elapsed_wall_s": 17.017191288992763
}
```
