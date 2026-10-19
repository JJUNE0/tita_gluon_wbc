# tita_flash_sac_193248_068255_model_85000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "6d6288767baeb4333ca248486f76da97d2a6aae106363217d0658fa81469cf4a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0030584768346491524,
  "max_drift_m": 0.042296000519306355,
  "radial_IAE_m_s": 0.3469124662700259,
  "signed_longitudinal_delta_m": 0.0030581496204526546,
  "tail_speed_mean_m_s": 0.00011058876381660822,
  "tail_speed_rms_m_s": 0.000953796639651784,
  "tail_sensor_speed_mean_m_s": 0.00011250376019103527,
  "tail_fk_speed_mean_m_s": 0.00011011614332240169,
  "peak_tilt_rad": 0.059403560383858744,
  "peak_wheel_torque_nm": 0.5822774171829224,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19020450469025665,
  "final_integral_m_s": 0.19020450469025665,
  "elapsed_wall_s": 6.200946621946059
}
```
