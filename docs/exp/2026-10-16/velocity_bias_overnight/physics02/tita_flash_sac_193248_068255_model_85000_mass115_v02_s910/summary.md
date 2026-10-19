# tita_flash_sac_193248_068255_model_85000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "dc0a5673c7c067afcdcafce16c8221e03955fccf5f0b6adaa1dffc9d2862756b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03176412941300527,
  "max_drift_m": 0.03182195997036853,
  "radial_IAE_m_s": 1.6181983985914417,
  "signed_longitudinal_delta_m": -0.03176211679725136,
  "tail_speed_mean_m_s": -0.0001619146574152731,
  "tail_speed_rms_m_s": 0.004536058965752224,
  "tail_sensor_speed_mean_m_s": -0.0004377106339903042,
  "tail_fk_speed_mean_m_s": 7.837924763446895e-05,
  "peak_tilt_rad": 0.09357864700543006,
  "peak_wheel_torque_nm": 2.486746072769165,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.20281249218090622,
  "final_integral_m_s": -0.2253745258632522,
  "elapsed_wall_s": 13.287917339999694
}
```
