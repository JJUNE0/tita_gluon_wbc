# tita_flash_sac_193248_068255_model_85000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_raw_s271",
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
    "estimator": "raw"
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
  "final_drift_m": 0.008146152096491839,
  "max_drift_m": 0.04146858184259987,
  "radial_IAE_m_s": 0.531456635770545,
  "signed_longitudinal_delta_m": 0.00814552051638469,
  "tail_speed_mean_m_s": -2.5840193456704022e-05,
  "tail_speed_rms_m_s": 0.005221314659910789,
  "tail_sensor_speed_mean_m_s": -0.0005499376796853573,
  "tail_fk_speed_mean_m_s": 2.3064860434191376e-05,
  "peak_tilt_rad": 0.06610409293443209,
  "peak_wheel_torque_nm": 1.3258540630340576,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.006863898567664707,
  "final_integral_m_s": 0.057844743904644745,
  "elapsed_wall_s": 4.3662316229892895
}
```
