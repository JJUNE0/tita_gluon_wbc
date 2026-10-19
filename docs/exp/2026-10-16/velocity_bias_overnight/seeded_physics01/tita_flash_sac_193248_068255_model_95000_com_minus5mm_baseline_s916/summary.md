# tita_flash_sac_193248_068255_model_95000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "7fa0d543cb7aa662ed258ccbcbb574c8982f0df1b9b9d64784bdd5f86f3dcff6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.316253253026606,
  "max_drift_m": 15.316253253026606,
  "radial_IAE_m_s": 450.6271607148964,
  "signed_longitudinal_delta_m": -14.493802447163047,
  "tail_speed_mean_m_s": -0.2640772707595668,
  "tail_speed_rms_m_s": 0.26409041672527916,
  "tail_sensor_speed_mean_m_s": -0.2636679605381692,
  "tail_fk_speed_mean_m_s": -0.26368002295609183,
  "peak_tilt_rad": 0.03622153531682892,
  "peak_wheel_torque_nm": 0.21846795082092285,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.175216857984196
}
```
