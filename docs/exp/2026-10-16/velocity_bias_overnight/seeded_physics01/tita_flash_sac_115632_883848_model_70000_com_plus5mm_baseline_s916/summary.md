# tita_flash_sac_115632_883848_model_70000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "3e747914673725abca4e0970d059433bfdcf2d9172f0c2cc41c24b6525e734ef",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.359236019608555,
  "max_drift_m": 3.359236019608555,
  "radial_IAE_m_s": 100.06261383269572,
  "signed_longitudinal_delta_m": -3.3551692611584225,
  "tail_speed_mean_m_s": -0.05629030957577122,
  "tail_speed_rms_m_s": 0.05629031039626781,
  "tail_sensor_speed_mean_m_s": -0.05616866210166478,
  "tail_fk_speed_mean_m_s": -0.05616867126092631,
  "peak_tilt_rad": 0.021859976692154337,
  "peak_wheel_torque_nm": 0.1306179016828537,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.567014522035606
}
```
