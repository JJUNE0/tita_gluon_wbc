# tita_flash_sac_193248_068255_model_90000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "66523d4c2ed3c9157748d5502fb99b001d89b00a53b9c58b722faa973a980a93",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 64.34451239772383,
  "max_drift_m": 64.34451239772383,
  "radial_IAE_m_s": 9791.327827759978,
  "signed_longitudinal_delta_m": 58.833632800033655,
  "tail_speed_mean_m_s": 0.22406428538995055,
  "tail_speed_rms_m_s": 0.2240642854012269,
  "tail_sensor_speed_mean_m_s": 0.22357943958631535,
  "tail_fk_speed_mean_m_s": 0.2235772354745839,
  "peak_tilt_rad": 0.11205967340663081,
  "peak_wheel_torque_nm": 1.952999234199524,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 55.73722421302227
}
```
