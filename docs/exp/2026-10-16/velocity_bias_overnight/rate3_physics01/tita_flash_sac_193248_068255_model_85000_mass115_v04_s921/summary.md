# tita_flash_sac_193248_068255_model_85000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "03eebffd86ad7f57c8c5be66858c8fbcedd4200ce73f2338425f117a2b027691",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006905231815977441,
  "max_drift_m": 0.02814818847679125,
  "radial_IAE_m_s": 0.524998888800413,
  "signed_longitudinal_delta_m": -0.006905126686831911,
  "tail_speed_mean_m_s": 4.2866921916577515e-05,
  "tail_speed_rms_m_s": 4.286928802075032e-05,
  "tail_sensor_speed_mean_m_s": 4.293275044782107e-05,
  "tail_fk_speed_mean_m_s": 4.23101340391838e-05,
  "peak_tilt_rad": 0.09314595453078023,
  "peak_wheel_torque_nm": 0.9585149884223938,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1204867262638687,
  "final_integral_m_s": -0.1204867262638687,
  "elapsed_wall_s": 7.972896557010245
}
```
