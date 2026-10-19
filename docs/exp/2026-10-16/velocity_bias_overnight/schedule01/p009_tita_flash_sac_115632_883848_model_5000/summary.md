# p009_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p009_tita_flash_sac_115632_883848_model_5000",
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
      "gain_velocity": 0.2,
      "gain_floor": 0.05
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
  "final_drift_m": 0.16936734397848574,
  "max_drift_m": 0.23072832029401277,
  "radial_IAE_m_s": 10.956878671917245,
  "signed_longitudinal_delta_m": -0.1693639676548809,
  "tail_speed_mean_m_s": 0.0006631327669843568,
  "tail_speed_rms_m_s": 0.0006660806182546288,
  "tail_sensor_speed_mean_m_s": 0.0006712622766775948,
  "tail_fk_speed_mean_m_s": 0.000675248257828413,
  "peak_tilt_rad": 0.1940504645586245,
  "peak_wheel_torque_nm": 3.885862350463867,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4513755032653336,
  "final_integral_m_s": -0.45143802638829766,
  "elapsed_wall_s": 12.700659114983864
}
```
