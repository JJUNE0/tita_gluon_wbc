# tita_flash_sac_193248_068255_model_85000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "c2d19e44b31992a5aac865807e1636ef461d52a0ef172727623c0e3f185e0b7c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06725075613282805,
  "max_drift_m": 0.0692469726163739,
  "radial_IAE_m_s": 3.1901830789520944,
  "signed_longitudinal_delta_m": -0.06723908336730804,
  "tail_speed_mean_m_s": -0.0005063258339086046,
  "tail_speed_rms_m_s": 0.013341251431080047,
  "tail_sensor_speed_mean_m_s": 0.0008025594829274284,
  "tail_fk_speed_mean_m_s": 8.631006256568665e-05,
  "peak_tilt_rad": 0.15304439170370032,
  "peak_wheel_torque_nm": 4.251639366149902,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3940692932169149,
  "final_integral_m_s": -0.3899253629815929,
  "elapsed_wall_s": 15.484064001007937
}
```
