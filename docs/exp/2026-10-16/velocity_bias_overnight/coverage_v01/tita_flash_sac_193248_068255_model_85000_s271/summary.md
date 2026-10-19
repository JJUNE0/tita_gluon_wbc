# tita_flash_sac_193248_068255_model_85000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "b5de2d1edc29af31880c7048005e554b939e77a01123cc73998f2530ce9b3d29",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.018342178949093804,
  "max_drift_m": 0.04384154131627282,
  "radial_IAE_m_s": 1.043289903460749,
  "signed_longitudinal_delta_m": 0.018342175621555736,
  "tail_speed_mean_m_s": 3.3799676245841056e-05,
  "tail_speed_rms_m_s": 3.382742467634815e-05,
  "tail_sensor_speed_mean_m_s": 3.384058410076648e-05,
  "tail_fk_speed_mean_m_s": 3.350273591148949e-05,
  "peak_tilt_rad": 0.06610409293443209,
  "peak_wheel_torque_nm": 0.8673127889633179,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1977766238659976,
  "final_integral_m_s": 0.1977131587517131,
  "elapsed_wall_s": 4.297869851987343
}
```
