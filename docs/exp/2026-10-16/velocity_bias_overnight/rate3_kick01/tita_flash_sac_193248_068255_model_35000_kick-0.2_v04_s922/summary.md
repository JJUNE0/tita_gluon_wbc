# tita_flash_sac_193248_068255_model_35000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "92e156d8018c080405033a898fde938b70a5e5180d69ba5e82b907b346fa81ca",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014963803269430654,
  "max_drift_m": 0.03805645296641298,
  "radial_IAE_m_s": 0.7887676668572794,
  "signed_longitudinal_delta_m": 0.01496079519346549,
  "tail_speed_mean_m_s": 7.129951796180307e-05,
  "tail_speed_rms_m_s": 7.130138826285717e-05,
  "tail_sensor_speed_mean_m_s": 7.094699247040983e-05,
  "tail_fk_speed_mean_m_s": 7.000629847341686e-05,
  "peak_tilt_rad": 0.05593865265295883,
  "peak_wheel_torque_nm": 1.0969560146331787,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30718647816712596,
  "final_integral_m_s": 0.30718647816712596,
  "elapsed_wall_s": 5.712485024007037
}
```
