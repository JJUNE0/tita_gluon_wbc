# tita_flash_sac_193248_068255_model_35000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "b4a18037bd85c04b2de0276f84b22e68365b2887e900ccc283d4ca77f1b2a714",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.472722587644478,
  "max_drift_m": 8.472722587644478,
  "radial_IAE_m_s": 240.83128196001977,
  "signed_longitudinal_delta_m": 8.376328414643648,
  "tail_speed_mean_m_s": 0.1541900873295361,
  "tail_speed_rms_m_s": 0.154198235523368,
  "tail_sensor_speed_mean_m_s": 0.1538577488558166,
  "tail_fk_speed_mean_m_s": 0.15384134758878712,
  "peak_tilt_rad": 0.07085518983386763,
  "peak_wheel_torque_nm": 1.1717185974121094,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.091583964007441
}
```
