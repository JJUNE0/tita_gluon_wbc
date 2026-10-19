# tita_flash_sac_115632_883848_model_5000_friction0.8_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_friction0.8_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
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
  "initial_physics_sha256": "e1ec80d8a87fdaefb677eda567076b89fc754a7c3139c4d77a76043b92aeea4e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04234254180822855,
  "max_drift_m": 0.08505689152012896,
  "radial_IAE_m_s": 2.687288478031207,
  "signed_longitudinal_delta_m": -0.04232789636144392,
  "tail_speed_mean_m_s": 2.1146798601496128e-05,
  "tail_speed_rms_m_s": 2.273473946399804e-05,
  "tail_sensor_speed_mean_m_s": 3.106651815928698e-05,
  "tail_fk_speed_mean_m_s": 3.519064139489694e-05,
  "peak_tilt_rad": 0.17822863509387976,
  "peak_wheel_torque_nm": 4.336061954498291,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4525485783244134,
  "final_integral_m_s": -0.4526101048256536,
  "elapsed_wall_s": 5.408867177029606
}
```
