# tita_flash_sac_193248_068255_model_70000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "97e7a9f3b2767c48a9b011e2677e0fb6777168cf72ad493a2e22b36d3a734273",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.296142358782038,
  "max_drift_m": 3.296142358782038,
  "radial_IAE_m_s": 99.3115940276559,
  "signed_longitudinal_delta_m": 3.2956398077950824,
  "tail_speed_mean_m_s": 0.05757264254906107,
  "tail_speed_rms_m_s": 0.0575901104152347,
  "tail_sensor_speed_mean_m_s": 0.0574486703420474,
  "tail_fk_speed_mean_m_s": 0.0574470977827315,
  "peak_tilt_rad": 0.09678249830377439,
  "peak_wheel_torque_nm": 1.5727813243865967,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.073977840016596
}
```
