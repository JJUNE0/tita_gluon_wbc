# tita_flash_sac_193248_068255_model_65000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "f67a190e92f81d6ff349a8d32e33ae1b988e9a536673d77c416ed89de7ea27cb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.943940594306097,
  "max_drift_m": 11.943940594306097,
  "radial_IAE_m_s": 358.15447223596937,
  "signed_longitudinal_delta_m": -11.827674510641659,
  "tail_speed_mean_m_s": -0.20019229210412984,
  "tail_speed_rms_m_s": 0.20019230565550433,
  "tail_sensor_speed_mean_m_s": -0.19977316455127367,
  "tail_fk_speed_mean_m_s": -0.19976954660684026,
  "peak_tilt_rad": 0.031141066080629942,
  "peak_wheel_torque_nm": 0.29543453454971313,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.212421818985604
}
```
