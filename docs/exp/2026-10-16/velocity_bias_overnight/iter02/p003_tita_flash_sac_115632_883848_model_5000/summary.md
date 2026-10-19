# p003_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p003_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 0.0,
      "ki": 5.0,
      "tau": 0.2,
      "ramp": 0.75,
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
  "final_drift_m": 0.08127230190018007,
  "max_drift_m": 0.1796154560598331,
  "radial_IAE_m_s": 5.577078281195652,
  "signed_longitudinal_delta_m": -0.08126590537305019,
  "tail_speed_mean_m_s": 0.00042077424064937907,
  "tail_speed_rms_m_s": 0.016445070067830532,
  "tail_sensor_speed_mean_m_s": 0.000466638920127559,
  "tail_fk_speed_mean_m_s": 0.00043940775686009587,
  "peak_tilt_rad": 0.19325916953173983,
  "peak_wheel_torque_nm": 3.9018115997314453,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3945581004096634,
  "final_integral_m_s": -0.3945581004096634,
  "elapsed_wall_s": 4.701080858008936
}
```
