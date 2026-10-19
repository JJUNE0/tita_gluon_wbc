# tita_flash_sac_193248_068255_model_35000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "1273387a48e36e30405337203b0fc15d336564bc8aac860d066a6c1650a1bdfd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.468188696252753,
  "max_drift_m": 7.468188696252753,
  "radial_IAE_m_s": 224.79961065196122,
  "signed_longitudinal_delta_m": -7.461485815901198,
  "tail_speed_mean_m_s": -0.12364626260464875,
  "tail_speed_rms_m_s": 0.12364660030709908,
  "tail_sensor_speed_mean_m_s": -0.1233807719780074,
  "tail_fk_speed_mean_m_s": -0.12337970807010547,
  "peak_tilt_rad": 0.029538430703168972,
  "peak_wheel_torque_nm": 0.37787842750549316,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 17.768521249992773
}
```
