# tita_flash_sac_193248_068255_model_85000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "c9262a3b00666f797b9fdf98f6b4145a82ae0a78141d1195f6b7bc81e47ea758",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.017749912669784505,
  "max_drift_m": 0.0422959867463011,
  "radial_IAE_m_s": 3.0245144151896612,
  "signed_longitudinal_delta_m": 0.017741763185047752,
  "tail_speed_mean_m_s": 5.041227884946883e-05,
  "tail_speed_rms_m_s": 5.0672908123520866e-05,
  "tail_sensor_speed_mean_m_s": 5.0460127931160445e-05,
  "tail_fk_speed_mean_m_s": 4.984030917452582e-05,
  "peak_tilt_rad": 0.05940355577593781,
  "peak_wheel_torque_nm": 0.5822703242301941,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24868581989479402,
  "final_integral_m_s": 0.24868581989479402,
  "elapsed_wall_s": 19.141288749000523
}
```
