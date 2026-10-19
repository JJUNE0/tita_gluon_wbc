# tita_flash_sac_193248_068255_model_35000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
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
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "eb69c781ef6c4ae4bf811fe264db9a6b06800b28c727cb4f23dc4493796eb332",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.083943708633711,
  "max_drift_m": 7.083943708633711,
  "radial_IAE_m_s": 202.82746208235653,
  "signed_longitudinal_delta_m": 7.03687558076941,
  "tail_speed_mean_m_s": 0.12881244728857127,
  "tail_speed_rms_m_s": 0.12882382325145192,
  "tail_sensor_speed_mean_m_s": 0.12853450589447293,
  "tail_fk_speed_mean_m_s": 0.12851878152599364,
  "peak_tilt_rad": 0.06506753753492411,
  "peak_wheel_torque_nm": 0.12393423914909363,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.774203351989854
}
```
