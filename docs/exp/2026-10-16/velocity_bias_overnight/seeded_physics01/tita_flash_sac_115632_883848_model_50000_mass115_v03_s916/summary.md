# tita_flash_sac_115632_883848_model_50000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "873cdb0b588372e38a303ccac6d54bbee1f6492d360454f845311aeb1341eb5b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005555090409361081,
  "max_drift_m": 0.028654907154466388,
  "radial_IAE_m_s": 0.3654462358738316,
  "signed_longitudinal_delta_m": 0.005431134023477757,
  "tail_speed_mean_m_s": -4.911753373612266e-06,
  "tail_speed_rms_m_s": 7.999156842423766e-06,
  "tail_sensor_speed_mean_m_s": -4.386906665956555e-06,
  "tail_fk_speed_mean_m_s": -2.8002800597940623e-06,
  "peak_tilt_rad": 0.10065012608810897,
  "peak_wheel_torque_nm": 0.5880739092826843,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.14273795673346015,
  "final_integral_m_s": -0.14273795673346015,
  "elapsed_wall_s": 13.794055127014872
}
```
