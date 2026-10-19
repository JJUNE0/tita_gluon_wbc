# tita_flash_sac_115632_883848_model_55000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "335daefa29059865bdb69441e297a0156b2cc359335e3f8c912835d857e3e32f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.8922305057513966,
  "max_drift_m": 2.2722881378993596,
  "radial_IAE_m_s": 94.17830234118367,
  "signed_longitudinal_delta_m": -0.4395722855565831,
  "tail_speed_mean_m_s": 0.09103613564879527,
  "tail_speed_rms_m_s": 0.0910383390748619,
  "tail_sensor_speed_mean_m_s": 0.09088439248880185,
  "tail_fk_speed_mean_m_s": 0.09092307516147496,
  "peak_tilt_rad": 0.08447717793761722,
  "peak_wheel_torque_nm": 0.1680946946144104,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.15359082899522
}
```
