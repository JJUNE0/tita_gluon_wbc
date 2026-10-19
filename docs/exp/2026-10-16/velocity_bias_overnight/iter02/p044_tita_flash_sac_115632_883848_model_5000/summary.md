# p044_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p044_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 10.0,
      "ki": 20.0,
      "tau": 0.05,
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
  "final_drift_m": 0.11745306856352986,
  "max_drift_m": 0.12040620075197593,
  "radial_IAE_m_s": 5.54375586312209,
  "signed_longitudinal_delta_m": -0.11711330494061446,
  "tail_speed_mean_m_s": -0.000816246903235743,
  "tail_speed_rms_m_s": 0.03110247155239796,
  "tail_sensor_speed_mean_m_s": 0.00039372314988149427,
  "tail_fk_speed_mean_m_s": 3.104492772316313e-05,
  "peak_tilt_rad": 0.08768645446223866,
  "peak_wheel_torque_nm": 4.2274699211120605,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.7480940420963187,
  "final_integral_m_s": -0.8707854956672069,
  "elapsed_wall_s": 4.80305478599621
}
```
