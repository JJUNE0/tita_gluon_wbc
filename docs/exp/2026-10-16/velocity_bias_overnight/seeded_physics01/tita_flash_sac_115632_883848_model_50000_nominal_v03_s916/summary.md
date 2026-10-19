# tita_flash_sac_115632_883848_model_50000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
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
  "initial_physics_sha256": "3b738209f23fca8df913ad3584027bbc7f2a2bd013397aa261627f8548d21194",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003314467195291377,
  "max_drift_m": 0.005997960039159071,
  "radial_IAE_m_s": 0.19986123683360424,
  "signed_longitudinal_delta_m": -0.0031984320801880825,
  "tail_speed_mean_m_s": 3.898192899257453e-06,
  "tail_speed_rms_m_s": 6.532154961894234e-06,
  "tail_sensor_speed_mean_m_s": 4.051926258392104e-06,
  "tail_fk_speed_mean_m_s": 6.484290761850479e-06,
  "peak_tilt_rad": 0.04186656221605589,
  "peak_wheel_torque_nm": 0.3228592574596405,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.02136577875364238,
  "final_integral_m_s": 0.02136577875364238,
  "elapsed_wall_s": 11.006207558966707
}
```
