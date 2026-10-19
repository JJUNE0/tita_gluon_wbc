# tita_flash_sac_193248_068255_model_95000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "eb967a15a73f17ba52e5e7cfc3c15b958cbaf2a035017e1a432db5aab5debee2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0151059470116969,
  "max_drift_m": 0.09009726556000189,
  "radial_IAE_m_s": 1.1702982495504521,
  "signed_longitudinal_delta_m": 0.015104515950422044,
  "tail_speed_mean_m_s": -1.7861762310840555e-06,
  "tail_speed_rms_m_s": 3.4315502472030014e-05,
  "tail_sensor_speed_mean_m_s": -1.3631286844810613e-06,
  "tail_fk_speed_mean_m_s": -2.0397212261025747e-06,
  "peak_tilt_rad": 0.08580959230927898,
  "peak_wheel_torque_nm": 0.6000389456748962,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23660062675240046,
  "final_integral_m_s": -0.23660062675240046,
  "elapsed_wall_s": 8.614488817984238
}
```
