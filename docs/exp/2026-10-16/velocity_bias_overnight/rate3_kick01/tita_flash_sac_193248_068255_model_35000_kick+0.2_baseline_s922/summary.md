# tita_flash_sac_193248_068255_model_35000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "c1f7a8db5b9149c17031a08b244777ac0ebe18ff34d41f56ec085101e05a6c09",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.804698773861631,
  "max_drift_m": 8.804698773861631,
  "radial_IAE_m_s": 259.6238146690922,
  "signed_longitudinal_delta_m": 8.704453752863365,
  "tail_speed_mean_m_s": 0.15464345081447414,
  "tail_speed_rms_m_s": 0.15465079405255314,
  "tail_sensor_speed_mean_m_s": 0.15431020693220185,
  "tail_fk_speed_mean_m_s": 0.15429369693609576,
  "peak_tilt_rad": 0.08911113576796192,
  "peak_wheel_torque_nm": 1.4000459909439087,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.282674847985618
}
```
