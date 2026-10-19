# tita_flash_sac_115632_883848_model_70000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "51a97a9f98a0d65a2894798cfa7a9a56c5d57a7a43781caa50989957b8ad21d7",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 22.70101716553718,
  "max_drift_m": 22.70101716553718,
  "radial_IAE_m_s": 3387.401326130943,
  "signed_longitudinal_delta_m": -21.523102410777536,
  "tail_speed_mean_m_s": -0.08040628040792572,
  "tail_speed_rms_m_s": 0.08040632914855651,
  "tail_sensor_speed_mean_m_s": -0.08027492833194945,
  "tail_fk_speed_mean_m_s": -0.08027319060378477,
  "peak_tilt_rad": 0.019425923456089622,
  "peak_wheel_torque_nm": 0.12323492765426636,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 55.197557172039524
}
```
