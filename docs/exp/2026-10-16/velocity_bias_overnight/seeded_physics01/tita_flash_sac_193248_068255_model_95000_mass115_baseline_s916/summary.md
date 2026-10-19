# tita_flash_sac_193248_068255_model_95000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "72f5893e2061276abf9878c4ddea29eb747a33a3f93970e2272f73b7ab248195",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.231083847645534,
  "max_drift_m": 14.231083847645534,
  "radial_IAE_m_s": 400.07055872102137,
  "signed_longitudinal_delta_m": -13.464328917983757,
  "tail_speed_mean_m_s": -0.2784844638260579,
  "tail_speed_rms_m_s": 0.27902625946961096,
  "tail_sensor_speed_mean_m_s": -0.2781941371629146,
  "tail_fk_speed_mean_m_s": -0.27818354165764503,
  "peak_tilt_rad": 0.06488053251714287,
  "peak_wheel_torque_nm": 0.3961900472640991,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.332548717968166
}
```
