# tita_flash_sac_193248_068255_model_35000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "98f08d08701ac4c2ecdb733b569df7a1980d7f1365eb5d489f5f0d1cff725f47",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 37.32184301394102,
  "max_drift_m": 37.32184301394102,
  "radial_IAE_m_s": 6209.680019570337,
  "signed_longitudinal_delta_m": 17.421468156673676,
  "tail_speed_mean_m_s": 0.16044795206941218,
  "tail_speed_rms_m_s": 0.16044795209341198,
  "tail_sensor_speed_mean_m_s": 0.16010011897424284,
  "tail_fk_speed_mean_m_s": 0.16008397136258692,
  "peak_tilt_rad": 0.07183408321132578,
  "peak_wheel_torque_nm": 0.12874263525009155,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 55.76372380700195
}
```
