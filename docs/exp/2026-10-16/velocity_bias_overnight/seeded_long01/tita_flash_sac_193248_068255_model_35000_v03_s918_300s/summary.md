# tita_flash_sac_193248_068255_model_35000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
  "initial_physics_sha256": "5f56b9fe59132c31ddf7dc7e1d0f1fbe0495412b61e1c79604a6f276d250ec30",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.02606563244952278,
  "max_drift_m": 0.040332987911295866,
  "radial_IAE_m_s": 6.352200695382884,
  "signed_longitudinal_delta_m": 0.026003345932263028,
  "tail_speed_mean_m_s": 7.375516751086151e-06,
  "tail_speed_rms_m_s": 7.3862818769249556e-06,
  "tail_sensor_speed_mean_m_s": 8.007217387800426e-06,
  "tail_fk_speed_mean_m_s": 6.265952459020892e-06,
  "peak_tilt_rad": 0.05787416571471482,
  "peak_wheel_torque_nm": 0.5622034072875977,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3441549802984787,
  "final_integral_m_s": 0.3441549802984787,
  "elapsed_wall_s": 55.28091480396688
}
```
