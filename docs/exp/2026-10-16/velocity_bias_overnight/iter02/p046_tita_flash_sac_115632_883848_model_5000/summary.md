# p046_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p046_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 10.0,
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
  "final_drift_m": 0.02387952799958852,
  "max_drift_m": 0.0746339039417765,
  "radial_IAE_m_s": 1.5027009169223042,
  "signed_longitudinal_delta_m": -0.023866062082550953,
  "tail_speed_mean_m_s": 4.0601158682642757e-05,
  "tail_speed_rms_m_s": 0.0032568511299508256,
  "tail_sensor_speed_mean_m_s": 8.628992855643671e-05,
  "tail_fk_speed_mean_m_s": 5.778226064765643e-05,
  "peak_tilt_rad": 0.16395769844387953,
  "peak_wheel_torque_nm": 4.273474216461182,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4158996626689361,
  "final_integral_m_s": -0.46456066843333355,
  "elapsed_wall_s": 4.989906774018891
}
```
