# tita_flash_sac_193248_068255_model_90000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "e902334d261a9f5685b2f65cdf1b0763db1b5de0213c4202b325749c81149928",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.131125127216044,
  "max_drift_m": 4.131125127216044,
  "radial_IAE_m_s": 125.61511155800164,
  "signed_longitudinal_delta_m": -4.130184154516565,
  "tail_speed_mean_m_s": -0.0669742097762401,
  "tail_speed_rms_m_s": 0.06898643511003638,
  "tail_sensor_speed_mean_m_s": -0.06695393622812312,
  "tail_fk_speed_mean_m_s": -0.06673743680346578,
  "peak_tilt_rad": 0.1267911158301649,
  "peak_wheel_torque_nm": 5.337335586547852,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.712839926010929
}
```
