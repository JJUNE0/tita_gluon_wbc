# tita_flash_sac_115632_883848_model_50000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "47b080e838d7d51461577bed1cf553aaf6b66279349a8d3e1ad5ac668b213e30",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0032337963046149367,
  "max_drift_m": 0.0056564701956182805,
  "radial_IAE_m_s": 0.19407413477664237,
  "signed_longitudinal_delta_m": -0.003143892189748746,
  "tail_speed_mean_m_s": 9.020060097213337e-07,
  "tail_speed_rms_m_s": 4.512511819129642e-06,
  "tail_sensor_speed_mean_m_s": 1.1121042262973308e-06,
  "tail_fk_speed_mean_m_s": 3.511120985021064e-06,
  "peak_tilt_rad": 0.04176193152829155,
  "peak_wheel_torque_nm": 0.34786802530288696,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.021362141723092615,
  "final_integral_m_s": 0.021362141723092615,
  "elapsed_wall_s": 15.928363095968962
}
```
