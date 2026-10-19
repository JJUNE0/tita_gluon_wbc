# tita_flash_sac_115632_883848_model_50000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "4ac873f1fbca167075e398d1e93efe0c26d927d37ca08e6783d7c255bd917c81",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.6843909085600427,
  "max_drift_m": 0.6843909085600427,
  "radial_IAE_m_s": 24.5730006400655,
  "signed_longitudinal_delta_m": 0.6748474618200218,
  "tail_speed_mean_m_s": 0.009341871700772955,
  "tail_speed_rms_m_s": 0.009342002524380772,
  "tail_sensor_speed_mean_m_s": 0.009321928826878118,
  "tail_fk_speed_mean_m_s": 0.009324147129711729,
  "peak_tilt_rad": 0.08115020356779201,
  "peak_wheel_torque_nm": 1.5053768157958984,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.488020075019449
}
```
