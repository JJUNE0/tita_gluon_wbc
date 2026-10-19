# tita_flash_sac_115632_883848_model_5000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_raw_s271",
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
    "estimator": "raw"
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
  "final_drift_m": 0.10562584993857256,
  "max_drift_m": 0.1596807635575305,
  "radial_IAE_m_s": 6.261031040231,
  "signed_longitudinal_delta_m": -0.10558454006244213,
  "tail_speed_mean_m_s": -0.00010550748920758176,
  "tail_speed_rms_m_s": 0.01191464235387928,
  "tail_sensor_speed_mean_m_s": -0.0003934842884413765,
  "tail_fk_speed_mean_m_s": 3.42748093535192e-06,
  "peak_tilt_rad": 0.2016769983599278,
  "peak_wheel_torque_nm": 4.228702068328857,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5908355864220699,
  "final_integral_m_s": -0.49214639913513236,
  "elapsed_wall_s": 4.863883426005486
}
```
