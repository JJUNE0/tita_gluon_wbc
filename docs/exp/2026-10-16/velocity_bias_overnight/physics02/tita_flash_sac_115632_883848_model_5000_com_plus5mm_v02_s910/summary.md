# tita_flash_sac_115632_883848_model_5000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "637283a5b2e9ddcead7b7916ba6b3b2a49dee1718c85341d1f9f634cd167da02",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.039669648511603775,
  "max_drift_m": 0.08346539382071333,
  "radial_IAE_m_s": 2.4709452725558414,
  "signed_longitudinal_delta_m": -0.039654903544939404,
  "tail_speed_mean_m_s": -9.27772247641346e-07,
  "tail_speed_rms_m_s": 5.507183602378038e-06,
  "tail_sensor_speed_mean_m_s": 7.452892996706471e-06,
  "tail_fk_speed_mean_m_s": 1.1335339553945034e-05,
  "peak_tilt_rad": 0.18040114775920224,
  "peak_wheel_torque_nm": 2.8841748237609863,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3906977513354054,
  "final_integral_m_s": -0.3907043464762235,
  "elapsed_wall_s": 19.34197576198494
}
```
