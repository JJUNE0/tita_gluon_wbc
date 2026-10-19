# tita_flash_sac_193248_068255_model_15000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "66d211663d0ba587fe5fa85642196c696a39f59d496d8cbb3a138e51235044fc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01642636003975576,
  "max_drift_m": 0.03156415110038703,
  "radial_IAE_m_s": 0.974036616387093,
  "signed_longitudinal_delta_m": -0.01642529845920141,
  "tail_speed_mean_m_s": -5.712553729536452e-06,
  "tail_speed_rms_m_s": 5.713933584642931e-06,
  "tail_sensor_speed_mean_m_s": -5.921441493295136e-06,
  "tail_fk_speed_mean_m_s": -3.6055314815679443e-06,
  "peak_tilt_rad": 0.08596904919104542,
  "peak_wheel_torque_nm": 2.5281031131744385,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1830727270040305,
  "final_integral_m_s": -0.18306557092319453,
  "elapsed_wall_s": 15.374542527948506
}
```
