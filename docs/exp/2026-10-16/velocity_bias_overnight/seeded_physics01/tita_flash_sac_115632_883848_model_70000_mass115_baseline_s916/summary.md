# tita_flash_sac_115632_883848_model_70000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "927d16fef0e66d2828acbaa40758170e4dae2f5ce93070ab189dcb744aa9f363",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.304052213333868,
  "max_drift_m": 8.304052213333868,
  "radial_IAE_m_s": 248.81919563899555,
  "signed_longitudinal_delta_m": -8.287920150359716,
  "tail_speed_mean_m_s": -0.1385332534514349,
  "tail_speed_rms_m_s": 0.13853327366767462,
  "tail_sensor_speed_mean_m_s": -0.13823453338968442,
  "tail_fk_speed_mean_m_s": -0.13823469451617362,
  "peak_tilt_rad": 0.016455563583530217,
  "peak_wheel_torque_nm": 0.1933349370956421,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.002947515051346
}
```
