# tita_flash_sac_193248_068255_model_35000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "30911b8afe93cbfd5f00b7c1cb28ba4d0f957c325dbccde837bb0663bbbf79c8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.64811442238439,
  "max_drift_m": 8.64811442238439,
  "radial_IAE_m_s": 250.56313056322077,
  "signed_longitudinal_delta_m": 8.54669297835058,
  "tail_speed_mean_m_s": 0.15450709381424105,
  "tail_speed_rms_m_s": 0.15451467700501675,
  "tail_sensor_speed_mean_m_s": 0.15417407289791082,
  "tail_fk_speed_mean_m_s": 0.15415764580584954,
  "peak_tilt_rad": 0.07089880627514478,
  "peak_wheel_torque_nm": 0.12893831729888916,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.317280410963576
}
```
