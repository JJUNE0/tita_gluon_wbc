# tita_flash_sac_193248_068255_model_95000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
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
  "initial_physics_sha256": "4214e53d3b1a71b63235a4b3a9ec511efcafe1b0c68cec6c11794829b9e987e6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 20.60255294216342,
  "max_drift_m": 20.60255294216342,
  "radial_IAE_m_s": 615.1117088312383,
  "signed_longitudinal_delta_m": -20.550457229753377,
  "tail_speed_mean_m_s": -0.3454803020085309,
  "tail_speed_rms_m_s": 0.3454803023700857,
  "tail_sensor_speed_mean_m_s": -0.34475448064318376,
  "tail_fk_speed_mean_m_s": -0.3447539118829423,
  "peak_tilt_rad": 0.06204705208952577,
  "peak_wheel_torque_nm": 0.5424129962921143,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.307533591985703
}
```
