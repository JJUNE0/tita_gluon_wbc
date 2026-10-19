# tita_flash_sac_115632_883848_model_70000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
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
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "3c66abb3500c9903df0f75f03a8e39427b134a5747ac35b134e050129d430f24",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0019676264052178004,
  "max_drift_m": 0.02334897379518471,
  "radial_IAE_m_s": 0.15729962071842593,
  "signed_longitudinal_delta_m": -0.0017908386138408535,
  "tail_speed_mean_m_s": 1.2764174708653477e-06,
  "tail_speed_rms_m_s": 4.0580204540246874e-06,
  "tail_sensor_speed_mean_m_s": 1.2228291263714878e-06,
  "tail_fk_speed_mean_m_s": 1.2866202543964382e-06,
  "peak_tilt_rad": 0.04093892460798387,
  "peak_wheel_torque_nm": 0.31212151050567627,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12259822804828273,
  "final_integral_m_s": -0.12259822804828273,
  "elapsed_wall_s": 4.670507941977121
}
```
