# tita_flash_sac_193248_068255_model_85000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "final_drift_m": 0.018550358727434175,
  "max_drift_m": 0.03157226155920133,
  "radial_IAE_m_s": 1.0346273014378093,
  "signed_longitudinal_delta_m": 0.018550214091462663,
  "tail_speed_mean_m_s": 3.961046004948026e-05,
  "tail_speed_rms_m_s": 3.9650298378286544e-05,
  "tail_sensor_speed_mean_m_s": 3.9643757110607064e-05,
  "tail_fk_speed_mean_m_s": 3.934429101270669e-05,
  "peak_tilt_rad": 0.05950865880466183,
  "peak_wheel_torque_nm": 0.780793309211731,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19085863994147637,
  "final_integral_m_s": 0.19079011809521182,
  "elapsed_wall_s": 17.385346914990805
}
```
