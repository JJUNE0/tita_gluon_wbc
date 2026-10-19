# tita_flash_sac_193248_068255_model_15000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "d22b1bc83042cb3900a441c977ec5ff4574194f36a8fdc5255ff66dd20f27361",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.4360182088404483,
  "max_drift_m": 3.4360182088404483,
  "radial_IAE_m_s": 103.38738601536961,
  "signed_longitudinal_delta_m": -3.4358575313325175,
  "tail_speed_mean_m_s": -0.05694334117811252,
  "tail_speed_rms_m_s": 0.05694341650150907,
  "tail_sensor_speed_mean_m_s": -0.056854109259674164,
  "tail_fk_speed_mean_m_s": -0.056853962128599875,
  "peak_tilt_rad": 0.04414397699370931,
  "peak_wheel_torque_nm": 0.07472512125968933,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.962969141022768
}
```
