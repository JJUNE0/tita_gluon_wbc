# tita_flash_sac_193248_068255_model_95000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "5ec74375d861563b6a882f426ef443c7058486b85355ccbf8b449ec5d5355a50",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021149047260384097,
  "max_drift_m": 0.040815351144808346,
  "radial_IAE_m_s": 1.2737099678326058,
  "signed_longitudinal_delta_m": -0.021142590775613517,
  "tail_speed_mean_m_s": 7.770864332066653e-07,
  "tail_speed_rms_m_s": 7.780900702625413e-07,
  "tail_sensor_speed_mean_m_s": 1.0363235407980814e-06,
  "tail_fk_speed_mean_m_s": 4.076309699100736e-07,
  "peak_tilt_rad": 0.07406247170598168,
  "peak_wheel_torque_nm": 1.643170714378357,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23640365554361384,
  "final_integral_m_s": -0.23640457547663968,
  "elapsed_wall_s": 11.815405118977651
}
```
