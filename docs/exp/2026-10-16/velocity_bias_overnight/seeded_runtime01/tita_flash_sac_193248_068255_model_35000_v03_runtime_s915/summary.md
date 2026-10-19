# tita_flash_sac_193248_068255_model_35000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "30f6342376d02b55d114d4d74a56ec54f564294ef18fcca699fa40b8d792c646",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015621354843094258,
  "max_drift_m": 0.04102754169879047,
  "radial_IAE_m_s": 0.8331836701232921,
  "signed_longitudinal_delta_m": 0.01562015171300266,
  "tail_speed_mean_m_s": 7.033329758731023e-05,
  "tail_speed_rms_m_s": 7.034012323620338e-05,
  "tail_sensor_speed_mean_m_s": 6.995523812271973e-05,
  "tail_fk_speed_mean_m_s": 6.900537229254161e-05,
  "peak_tilt_rad": 0.058649527540768354,
  "peak_wheel_torque_nm": 0.5786125063896179,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30984177009083036,
  "final_integral_m_s": 0.30984177009083036,
  "elapsed_wall_s": 16.637145696033258
}
```
