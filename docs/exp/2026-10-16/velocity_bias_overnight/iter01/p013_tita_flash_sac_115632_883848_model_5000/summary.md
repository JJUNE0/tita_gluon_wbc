# p013_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p013_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 2.0,
      "ki": 0.5,
      "tau": 0.5,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 1.0,
      "ramp": 1.5
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
  "final_drift_m": 0.9588072066886103,
  "max_drift_m": 1.534440135462471,
  "radial_IAE_m_s": 64.99527903004919,
  "signed_longitudinal_delta_m": -0.9587256495271779,
  "tail_speed_mean_m_s": 0.0071657548837260315,
  "tail_speed_rms_m_s": 0.008720847022397416,
  "tail_sensor_speed_mean_m_s": 0.007154783672340008,
  "tail_fk_speed_mean_m_s": 0.007166557024296864,
  "peak_tilt_rad": 0.1860063222303301,
  "peak_wheel_torque_nm": 3.8526573181152344,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.47461525865420967,
  "final_integral_m_s": -0.4782489775541143,
  "elapsed_wall_s": 4.69919698801823
}
```
