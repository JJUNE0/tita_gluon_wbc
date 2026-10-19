# p005_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p005_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": -2.0,
      "ki": 5.0,
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
  "final_drift_m": 0.5005272366925243,
  "max_drift_m": 0.5862340687046202,
  "radial_IAE_m_s": 19.9115997004971,
  "signed_longitudinal_delta_m": -0.2128277750157464,
  "tail_speed_mean_m_s": -0.037217290947041876,
  "tail_speed_rms_m_s": 0.27608688031407747,
  "tail_sensor_speed_mean_m_s": -0.041222892732675126,
  "tail_fk_speed_mean_m_s": -0.03713222360824092,
  "peak_tilt_rad": 0.29221146784537777,
  "peak_wheel_torque_nm": 4.9794487953186035,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.047799052016878,
  "final_integral_m_s": -2.0,
  "elapsed_wall_s": 4.798642809037119
}
```
