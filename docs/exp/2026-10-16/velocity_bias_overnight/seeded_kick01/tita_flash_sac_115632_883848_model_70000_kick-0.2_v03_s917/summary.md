# tita_flash_sac_115632_883848_model_70000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "58a73f2ccfc1e6331a7b6879b7ddde5ef3aeaa1ea082603dcf5ede580d918689",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005418948210882183,
  "max_drift_m": 0.11577073221595904,
  "radial_IAE_m_s": 0.5550628934334904,
  "signed_longitudinal_delta_m": 0.005347302827146841,
  "tail_speed_mean_m_s": 4.227748399133103e-06,
  "tail_speed_rms_m_s": 6.600192930731372e-06,
  "tail_sensor_speed_mean_m_s": 4.179359585288481e-06,
  "tail_fk_speed_mean_m_s": 4.234691392051168e-06,
  "peak_tilt_rad": 0.09396743864508439,
  "peak_wheel_torque_nm": 1.870053768157959,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12260064516719112,
  "final_integral_m_s": -0.12260064516719112,
  "elapsed_wall_s": 11.753996530955192
}
```
