# tita_flash_sac_115632_883848_model_95000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "35ac83a3997ddd440d97cb7e19594e00be39957605e65735c1309c541dc9e5a0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.337490931785803,
  "max_drift_m": 11.337490931785803,
  "radial_IAE_m_s": 342.55150232062647,
  "signed_longitudinal_delta_m": -11.337109923063922,
  "tail_speed_mean_m_s": -0.18578513989661574,
  "tail_speed_rms_m_s": 0.18578967549930173,
  "tail_sensor_speed_mean_m_s": -0.18538556288782085,
  "tail_fk_speed_mean_m_s": -0.18538603743774104,
  "peak_tilt_rad": 0.038717539320108685,
  "peak_wheel_torque_nm": 0.5306258201599121,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.796507816005033
}
```
