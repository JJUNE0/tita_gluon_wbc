# tita_flash_sac_193248_068255_model_95000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "25cff5f637bb353084fb852cb7826f58b8541add147af60a0538fdd01b5fd20a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021467367182683487,
  "max_drift_m": 0.04647757636197602,
  "radial_IAE_m_s": 1.295553554070294,
  "signed_longitudinal_delta_m": -0.02146616944717296,
  "tail_speed_mean_m_s": 1.3395567184774589e-06,
  "tail_speed_rms_m_s": 1.3407212067014472e-06,
  "tail_sensor_speed_mean_m_s": 1.3013211140395552e-06,
  "tail_fk_speed_mean_m_s": 6.317868580311128e-07,
  "peak_tilt_rad": 0.07536845741447329,
  "peak_wheel_torque_nm": 0.4992997944355011,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.225333610651893,
  "final_integral_m_s": -0.22533498887872172,
  "elapsed_wall_s": 26.757479664986022
}
```
