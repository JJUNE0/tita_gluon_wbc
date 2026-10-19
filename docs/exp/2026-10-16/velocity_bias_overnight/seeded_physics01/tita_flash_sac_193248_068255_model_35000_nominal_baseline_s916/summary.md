# tita_flash_sac_193248_068255_model_35000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
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
  "initial_physics_sha256": "1b4ff07f8be80de1fdfae8af88eb5a9632d078d5271cf1ad8d6c3d8eebdd94d4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.612371760671076,
  "max_drift_m": 8.612371760671076,
  "radial_IAE_m_s": 249.18814924444578,
  "signed_longitudinal_delta_m": 8.520525012173728,
  "tail_speed_mean_m_s": 0.15416976579840647,
  "tail_speed_rms_m_s": 0.15417795326081082,
  "tail_sensor_speed_mean_m_s": 0.153837450428568,
  "tail_fk_speed_mean_m_s": 0.15382107183391633,
  "peak_tilt_rad": 0.07085236360767211,
  "peak_wheel_torque_nm": 0.1279442310333252,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.233403642952908
}
```
