# tita_flash_sac_115632_883848_model_50000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "fd318ef849cb5a1169e1265fd0c8c412a6a2d9a062885478034c94a53342c576",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0017212023164119607,
  "max_drift_m": 0.003363737507252699,
  "radial_IAE_m_s": 0.10405983792246828,
  "signed_longitudinal_delta_m": 0.0015922806752538476,
  "tail_speed_mean_m_s": -2.143651378764294e-06,
  "tail_speed_rms_m_s": 2.2532666151635585e-06,
  "tail_sensor_speed_mean_m_s": -1.9012070507728964e-06,
  "tail_fk_speed_mean_m_s": 4.7598458376822967e-07,
  "peak_tilt_rad": 0.039719960739055704,
  "peak_wheel_torque_nm": 0.34479212760925293,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.02134960819204636,
  "final_integral_m_s": 0.021350570144869727,
  "elapsed_wall_s": 4.382243844040204
}
```
