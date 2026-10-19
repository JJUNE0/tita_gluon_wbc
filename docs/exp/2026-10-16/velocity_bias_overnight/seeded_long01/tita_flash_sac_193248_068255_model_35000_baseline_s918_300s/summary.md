# tita_flash_sac_193248_068255_model_35000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "5f56b9fe59132c31ddf7dc7e1d0f1fbe0495412b61e1c79604a6f276d250ec30",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 37.31812245023036,
  "max_drift_m": 37.31812245023036,
  "radial_IAE_m_s": 6205.255930846336,
  "signed_longitudinal_delta_m": 17.59035976371872,
  "tail_speed_mean_m_s": 0.16044793982094174,
  "tail_speed_rms_m_s": 0.16044793984460304,
  "tail_sensor_speed_mean_m_s": 0.16010011224031687,
  "tail_fk_speed_mean_m_s": 0.16008395854544974,
  "peak_tilt_rad": 0.07183408176131989,
  "peak_wheel_torque_nm": 0.12794089317321777,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 56.82564136298606
}
```
