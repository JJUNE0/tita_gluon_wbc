# tita_flash_sac_193248_068255_model_95000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
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
  "final_drift_m": 0.013950318611852103,
  "max_drift_m": 0.13034855487788474,
  "radial_IAE_m_s": 1.325343644576509,
  "signed_longitudinal_delta_m": 0.013950306296577597,
  "tail_speed_mean_m_s": 0.00019330312499607732,
  "tail_speed_rms_m_s": 0.001659549291921785,
  "tail_sensor_speed_mean_m_s": 0.00020367268004261837,
  "tail_fk_speed_mean_m_s": 0.00019243747602821302,
  "peak_tilt_rad": 0.09747429286754805,
  "peak_wheel_torque_nm": 0.42044326663017273,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3582471075399587,
  "final_integral_m_s": -0.3582471075399587,
  "elapsed_wall_s": 10.260423284024
}
```
