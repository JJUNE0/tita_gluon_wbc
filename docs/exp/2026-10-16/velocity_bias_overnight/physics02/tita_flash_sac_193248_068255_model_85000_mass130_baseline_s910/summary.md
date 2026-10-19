# tita_flash_sac_193248_068255_model_85000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 12.848456919240075,
  "max_drift_m": 12.848456919240075,
  "radial_IAE_m_s": 380.8513085011514,
  "signed_longitudinal_delta_m": -12.848025016763563,
  "tail_speed_mean_m_s": -0.21821713777965893,
  "tail_speed_rms_m_s": 0.21822188660150582,
  "tail_sensor_speed_mean_m_s": -0.21782554854581818,
  "tail_fk_speed_mean_m_s": -0.2178272095278737,
  "peak_tilt_rad": 0.0871435881795859,
  "peak_wheel_torque_nm": 1.2667970657348633,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.77241066202987
}
```
