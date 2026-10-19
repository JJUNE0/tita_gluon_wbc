# tita_flash_sac_115632_883848_model_50000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_raw_s271",
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
    "estimator": "raw"
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
  "final_drift_m": 0.0015449234837054658,
  "max_drift_m": 0.004452412068212167,
  "radial_IAE_m_s": 0.16396251307653767,
  "signed_longitudinal_delta_m": 0.0013629041507443648,
  "tail_speed_mean_m_s": -4.400814110791674e-05,
  "tail_speed_rms_m_s": 0.004834450215786128,
  "tail_sensor_speed_mean_m_s": -0.00019120332594202495,
  "tail_fk_speed_mean_m_s": -1.406286877173803e-05,
  "peak_tilt_rad": 0.04361283508449754,
  "peak_wheel_torque_nm": 1.036201000213623,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11285727994916611,
  "final_integral_m_s": 0.009188005049865076,
  "elapsed_wall_s": 4.466229968005791
}
```
