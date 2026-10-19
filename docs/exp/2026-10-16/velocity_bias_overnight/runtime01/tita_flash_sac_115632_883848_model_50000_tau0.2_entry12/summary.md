# tita_flash_sac_115632_883848_model_50000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "644abcdf1529f758fc08fc4a92a14317c41eb4bedccac35a08d37573658c1c1c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0016940501428347704,
  "max_drift_m": 0.004423192807084007,
  "radial_IAE_m_s": 0.10043052559728996,
  "signed_longitudinal_delta_m": 0.0014641135816851716,
  "tail_speed_mean_m_s": -2.4407667774542315e-07,
  "tail_speed_rms_m_s": 2.0736324153971745e-06,
  "tail_sensor_speed_mean_m_s": -6.816986256438745e-08,
  "tail_fk_speed_mean_m_s": 2.3544938911139086e-06,
  "peak_tilt_rad": 0.04181293427134136,
  "peak_wheel_torque_nm": 0.3042401969432831,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.021377339157422005,
  "final_integral_m_s": 0.021375386208485656,
  "elapsed_wall_s": 6.00326272303937
}
```
