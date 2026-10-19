# tita_flash_sac_193248_068255_model_95000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 4.531151274377185,
  "max_drift_m": 4.531151274377185,
  "radial_IAE_m_s": 135.46929544091117,
  "signed_longitudinal_delta_m": -4.523580820796092,
  "tail_speed_mean_m_s": -0.0760900954013954,
  "tail_speed_rms_m_s": 0.0760901848846695,
  "tail_sensor_speed_mean_m_s": -0.07596416435635464,
  "tail_fk_speed_mean_m_s": -0.07596627085235964,
  "peak_tilt_rad": 0.04871574948971946,
  "peak_wheel_torque_nm": 0.2504609227180481,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.024324421014171
}
```
