# tita_flash_sac_115632_883848_model_95000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
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
  "final_drift_m": 0.06414003403984807,
  "max_drift_m": 0.1110496182749145,
  "radial_IAE_m_s": 3.8786976872311794,
  "signed_longitudinal_delta_m": -0.0641374926576417,
  "tail_speed_mean_m_s": 5.574129711866368e-06,
  "tail_speed_rms_m_s": 5.574902074794476e-06,
  "tail_sensor_speed_mean_m_s": 5.414808625234975e-06,
  "tail_fk_speed_mean_m_s": 4.994083718878632e-06,
  "peak_tilt_rad": 0.1553166932497403,
  "peak_wheel_torque_nm": 1.114500880241394,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.7499240184434388,
  "final_integral_m_s": -0.7499240184434388,
  "elapsed_wall_s": 13.690041702007875
}
```
