# tita_flash_sac_193248_068255_model_95000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
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
  "initial_physics_sha256": "d15ccf22dd2c6f274219ac4d175bf340c489ca727d1960c7067ed2b703695d6a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022205618209775336,
  "max_drift_m": 0.05950269717705417,
  "radial_IAE_m_s": 1.3367720732611414,
  "signed_longitudinal_delta_m": -0.022201604872959375,
  "tail_speed_mean_m_s": 6.79656836353464e-07,
  "tail_speed_rms_m_s": 6.812598098205976e-07,
  "tail_sensor_speed_mean_m_s": 9.760993934062612e-07,
  "tail_fk_speed_mean_m_s": 3.413403248376281e-07,
  "peak_tilt_rad": 0.08575306550265083,
  "peak_wheel_torque_nm": 0.4737757444381714,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23725871054408407,
  "final_integral_m_s": -0.23725941568434097,
  "elapsed_wall_s": 4.398656452016439
}
```
