# tita_flash_sac_193248_068255_model_85000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "a7bc00bd3fa6638c2654b42ec62d60e77efc28483d369f759f13b823e121aac6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020368031043617375,
  "max_drift_m": 0.15370531455667308,
  "radial_IAE_m_s": 1.7923575898165445,
  "signed_longitudinal_delta_m": -0.020367543018402556,
  "tail_speed_mean_m_s": 0.00013482256522766284,
  "tail_speed_rms_m_s": 0.0007326557116550432,
  "tail_sensor_speed_mean_m_s": 0.00013896006133517577,
  "tail_fk_speed_mean_m_s": 0.00013428834741426957,
  "peak_tilt_rad": 0.07457670028314767,
  "peak_wheel_torque_nm": 1.6132041215896606,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19293869042694572,
  "final_integral_m_s": 0.19293869042694572,
  "elapsed_wall_s": 12.165707345993724
}
```
