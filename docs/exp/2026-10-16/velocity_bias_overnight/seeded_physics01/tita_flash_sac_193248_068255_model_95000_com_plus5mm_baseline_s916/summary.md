# tita_flash_sac_193248_068255_model_95000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "d5fede61dd3913e37a7b870c3381b6f2fdbf449b5f6351d065b0ca0f5e5109af",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.7508070770763812,
  "max_drift_m": 0.7508070770763812,
  "radial_IAE_m_s": 25.294588725195023,
  "signed_longitudinal_delta_m": -0.7507686765876068,
  "tail_speed_mean_m_s": -0.010707160835612656,
  "tail_speed_rms_m_s": 0.010707785076848495,
  "tail_sensor_speed_mean_m_s": -0.010683851836637693,
  "tail_fk_speed_mean_m_s": -0.010684328678229545,
  "peak_tilt_rad": 0.06035436701237917,
  "peak_wheel_torque_nm": 0.23835791647434235,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.90871322300518
}
```
