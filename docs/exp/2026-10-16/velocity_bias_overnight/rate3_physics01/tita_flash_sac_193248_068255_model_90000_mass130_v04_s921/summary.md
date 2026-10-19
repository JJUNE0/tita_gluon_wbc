# tita_flash_sac_193248_068255_model_90000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "19b119a7779946d128029b41bd6a5f32fbfd22630bd6e43a4e8a217c6173cf7c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00521151483669762,
  "max_drift_m": 0.038958905748093804,
  "radial_IAE_m_s": 0.8397790712796187,
  "signed_longitudinal_delta_m": 0.005095017490052962,
  "tail_speed_mean_m_s": -0.0002928515416971476,
  "tail_speed_rms_m_s": 0.015607053118292052,
  "tail_sensor_speed_mean_m_s": -0.0023064108731756373,
  "tail_fk_speed_mean_m_s": -7.55064689870619e-05,
  "peak_tilt_rad": 0.1633511226240716,
  "peak_wheel_torque_nm": 5.29948091506958,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.13657102527835685,
  "final_integral_m_s": -0.13657102527835685,
  "elapsed_wall_s": 8.93827354698442
}
```
