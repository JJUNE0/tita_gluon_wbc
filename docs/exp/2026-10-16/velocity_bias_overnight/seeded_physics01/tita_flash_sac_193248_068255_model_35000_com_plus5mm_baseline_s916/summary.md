# tita_flash_sac_193248_068255_model_35000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
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
  "initial_physics_sha256": "12c6960ad475dd1fd726c7d4570748ef5b2a69d3de4cb5851e4cc528b429b73e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.296496955719826,
  "max_drift_m": 10.296496955719826,
  "radial_IAE_m_s": 301.0459925513984,
  "signed_longitudinal_delta_m": 10.113335597443463,
  "tail_speed_mean_m_s": 0.1813767527997069,
  "tail_speed_rms_m_s": 0.18137861231766284,
  "tail_sensor_speed_mean_m_s": 0.18098564823501967,
  "tail_fk_speed_mean_m_s": 0.18097017198720466,
  "peak_tilt_rad": 0.07615686190094251,
  "peak_wheel_torque_nm": 0.12997758388519287,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.689731271006167
}
```
