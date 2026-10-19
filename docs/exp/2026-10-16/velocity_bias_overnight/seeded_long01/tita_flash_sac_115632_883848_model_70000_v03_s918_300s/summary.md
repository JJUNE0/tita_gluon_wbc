# tita_flash_sac_115632_883848_model_70000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
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
  "final_drift_m": 0.0022260124977897837,
  "max_drift_m": 0.02346410718417762,
  "radial_IAE_m_s": 0.6088421239847466,
  "signed_longitudinal_delta_m": -0.0016999574738892013,
  "tail_speed_mean_m_s": -4.627395535304554e-06,
  "tail_speed_rms_m_s": 4.925514966823444e-06,
  "tail_sensor_speed_mean_m_s": -4.615095458008652e-06,
  "tail_fk_speed_mean_m_s": -4.76561023800197e-06,
  "peak_tilt_rad": 0.04149298368545806,
  "peak_wheel_torque_nm": 0.31728827953338623,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12318997080965378,
  "final_integral_m_s": -0.12318997080965378,
  "elapsed_wall_s": 53.203136475000065
}
```
