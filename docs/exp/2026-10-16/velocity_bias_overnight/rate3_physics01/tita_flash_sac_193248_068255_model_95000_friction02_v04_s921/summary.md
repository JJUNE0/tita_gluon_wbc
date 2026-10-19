# tita_flash_sac_193248_068255_model_95000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "dc74481e873d15e94750b18a337c432cf3c02194afd8a315133f28570df8a722",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0009593049314448219,
  "max_drift_m": 0.05309066508713397,
  "radial_IAE_m_s": 0.28655021405774006,
  "signed_longitudinal_delta_m": 0.0009552004562607809,
  "tail_speed_mean_m_s": 3.1438929271438236e-06,
  "tail_speed_rms_m_s": 5.013908892855736e-06,
  "tail_sensor_speed_mean_m_s": 3.12988090767763e-06,
  "tail_fk_speed_mean_m_s": 2.4332591441999346e-06,
  "peak_tilt_rad": 0.07577277193194809,
  "peak_wheel_torque_nm": 0.5175483822822571,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.22531815277852427,
  "final_integral_m_s": -0.22531815277852427,
  "elapsed_wall_s": 9.8209372839774
}
```
