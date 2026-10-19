# tita_flash_sac_115632_883848_model_70000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "cb289ec60993a46cbf339cea5ed09176fdb34b8b884f507e5191ceb92e457530",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0016791218726717027,
  "max_drift_m": 0.02346414168785094,
  "radial_IAE_m_s": 0.14587901745866305,
  "signed_longitudinal_delta_m": -0.0014632735124574994,
  "tail_speed_mean_m_s": 7.444057903733461e-06,
  "tail_speed_rms_m_s": 8.423304053431626e-06,
  "tail_sensor_speed_mean_m_s": 7.391219508473556e-06,
  "tail_fk_speed_mean_m_s": 7.446522032034542e-06,
  "peak_tilt_rad": 0.04149297910159322,
  "peak_wheel_torque_nm": 0.31728631258010864,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12259546649190124,
  "final_integral_m_s": -0.12259546649190124,
  "elapsed_wall_s": 9.09790123597486
}
```
