# tita_flash_sac_193248_068255_model_95000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "9bad2fd21e173e5fa762c31013a3ba0187843391a383957e787ef9bba8406ac9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009763018496236868,
  "max_drift_m": 0.20505452557678946,
  "radial_IAE_m_s": 1.5271345185440248,
  "signed_longitudinal_delta_m": 0.009598088304350171,
  "tail_speed_mean_m_s": -5.360354660279474e-06,
  "tail_speed_rms_m_s": 6.0081573004764754e-05,
  "tail_sensor_speed_mean_m_s": -5.6240034204418894e-06,
  "tail_fk_speed_mean_m_s": -5.7311566425416466e-06,
  "peak_tilt_rad": 0.13050284788379596,
  "peak_wheel_torque_nm": 1.7496695518493652,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23665555784695522,
  "final_integral_m_s": -0.23665555784695522,
  "elapsed_wall_s": 16.391985566995572
}
```
