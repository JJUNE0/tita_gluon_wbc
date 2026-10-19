# tita_flash_sac_193248_068255_model_85000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "75da87c684b9c323b00f3fe603a1d5e10f5bbc360a5984710a685ac946f00084",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.9760930286779734,
  "max_drift_m": 3.9760930286779734,
  "radial_IAE_m_s": 107.6686110158654,
  "signed_longitudinal_delta_m": 3.974310999409735,
  "tail_speed_mean_m_s": 0.07759633340899114,
  "tail_speed_rms_m_s": 0.07762440173585775,
  "tail_sensor_speed_mean_m_s": 0.07742874139106404,
  "tail_fk_speed_mean_m_s": 0.07742616329727965,
  "peak_tilt_rad": 0.06343027312298077,
  "peak_wheel_torque_nm": 0.38624003529548645,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.97683836700162
}
```
