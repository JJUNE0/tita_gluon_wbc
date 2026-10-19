# tita_flash_sac_193248_068255_model_70000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
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
  "initial_physics_sha256": "8cb0c8e485a8899dea60546a129843852777d370f320fddde9f387df2ebb311e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010991049509347437,
  "max_drift_m": 0.014789731035358493,
  "radial_IAE_m_s": 0.5474797375668603,
  "signed_longitudinal_delta_m": 0.010991049443422773,
  "tail_speed_mean_m_s": 5.9636137472471466e-05,
  "tail_speed_rms_m_s": 5.963950094168948e-05,
  "tail_sensor_speed_mean_m_s": 5.963588310128935e-05,
  "tail_fk_speed_mean_m_s": 5.9357981114080164e-05,
  "peak_tilt_rad": 0.07573398416829424,
  "peak_wheel_torque_nm": 0.10990414768457413,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0887243851036629,
  "final_integral_m_s": 0.0887243851036629,
  "elapsed_wall_s": 4.755732175020967
}
```
