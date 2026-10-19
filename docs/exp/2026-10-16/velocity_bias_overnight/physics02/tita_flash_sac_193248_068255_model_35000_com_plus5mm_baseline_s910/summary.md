# tita_flash_sac_193248_068255_model_35000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "b46c15ec6eb9f164ab038148a3f2ff1c90589aca7ac5e414a36c6a081712ec59",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.062462225110105,
  "max_drift_m": 10.062462225110105,
  "radial_IAE_m_s": 291.36380328016827,
  "signed_longitudinal_delta_m": 9.965754925125315,
  "tail_speed_mean_m_s": 0.17986675987289538,
  "tail_speed_rms_m_s": 0.1798722259044923,
  "tail_sensor_speed_mean_m_s": 0.17947917899866006,
  "tail_fk_speed_mean_m_s": 0.17946361073511022,
  "peak_tilt_rad": 0.07595636630450864,
  "peak_wheel_torque_nm": 0.1287921667098999,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 17.00078191101784
}
```
