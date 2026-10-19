# tita_flash_sac_193248_068255_model_85000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "a8c25717ef3266bd233535218686aa1a2b6be2b5366fea0c8a71b23efbb8d345",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03196559698728853,
  "max_drift_m": 0.06720373329295751,
  "radial_IAE_m_s": 1.4002100206180947,
  "signed_longitudinal_delta_m": -0.03195257681513661,
  "tail_speed_mean_m_s": -0.0003654650853709586,
  "tail_speed_rms_m_s": 0.010565161234431868,
  "tail_sensor_speed_mean_m_s": -0.0001462966476214164,
  "tail_fk_speed_mean_m_s": 0.00014876590551502424,
  "peak_tilt_rad": 0.15558913172562638,
  "peak_wheel_torque_nm": 3.5117380619049072,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3955963988503166,
  "final_integral_m_s": -0.3955963988503166,
  "elapsed_wall_s": 6.839121139026247
}
```
