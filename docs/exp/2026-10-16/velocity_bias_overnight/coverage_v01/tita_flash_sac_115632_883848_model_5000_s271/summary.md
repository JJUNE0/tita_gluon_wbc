# tita_flash_sac_115632_883848_model_5000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
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
  "initial_physics_sha256": "70226b3547f426c19cc13df4523ed7466beae60e11dfe053992b92d6116e2871",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.042862662237966406,
  "max_drift_m": 0.08445989238136584,
  "radial_IAE_m_s": 2.713215524804845,
  "signed_longitudinal_delta_m": -0.04284720688204299,
  "tail_speed_mean_m_s": 1.8445447080772797e-05,
  "tail_speed_rms_m_s": 1.9681572791069238e-05,
  "tail_sensor_speed_mean_m_s": 3.0521973092834746e-05,
  "tail_fk_speed_mean_m_s": 3.4848330400906276e-05,
  "peak_tilt_rad": 0.17618011210516005,
  "peak_wheel_torque_nm": 4.300508975982666,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4572392853994875,
  "final_integral_m_s": -0.45732284212858515,
  "elapsed_wall_s": 5.202147927950136
}
```
