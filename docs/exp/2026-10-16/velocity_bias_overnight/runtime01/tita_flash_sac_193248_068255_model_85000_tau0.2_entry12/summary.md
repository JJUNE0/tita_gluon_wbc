# tita_flash_sac_193248_068255_model_85000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "initial_physics_sha256": "b42a626ea5fafeb89c4473eb656ace99d03eaf8d765835b8c6b98a379aff836b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.018573913016760764,
  "max_drift_m": 0.037871514355307105,
  "radial_IAE_m_s": 1.0328822747196371,
  "signed_longitudinal_delta_m": 0.018573786296480068,
  "tail_speed_mean_m_s": 4.011433704592741e-05,
  "tail_speed_rms_m_s": 4.2639145301680074e-05,
  "tail_sensor_speed_mean_m_s": 4.0338939010035234e-05,
  "tail_fk_speed_mean_m_s": 3.98463325270915e-05,
  "peak_tilt_rad": 0.05950865880466183,
  "peak_wheel_torque_nm": 0.5328412652015686,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1909398992724285,
  "final_integral_m_s": 0.1908716272964933,
  "elapsed_wall_s": 20.657172195031308
}
```
