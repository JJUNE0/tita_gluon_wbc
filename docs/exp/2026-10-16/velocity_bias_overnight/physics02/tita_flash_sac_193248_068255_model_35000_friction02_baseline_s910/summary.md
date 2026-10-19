# tita_flash_sac_193248_068255_model_35000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "5a01404f95ea6640dd668904bced13c307a20c4622d0dea9652a8552f74a9f31",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.574721129030237,
  "max_drift_m": 9.574721129030237,
  "radial_IAE_m_s": 289.3435086541143,
  "signed_longitudinal_delta_m": 9.02711633725975,
  "tail_speed_mean_m_s": 0.16335703798917034,
  "tail_speed_rms_m_s": 0.1633570383193093,
  "tail_sensor_speed_mean_m_s": 0.16294062220413036,
  "tail_fk_speed_mean_m_s": 0.16291535984607236,
  "peak_tilt_rad": 0.07286049349474921,
  "peak_wheel_torque_nm": 0.1476895809173584,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.685047293023672
}
```
