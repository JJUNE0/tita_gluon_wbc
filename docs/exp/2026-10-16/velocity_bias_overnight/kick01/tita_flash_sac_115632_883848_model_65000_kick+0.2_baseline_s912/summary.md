# tita_flash_sac_115632_883848_model_65000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
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
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "e6bb68f059323e1c520a739dc868454afe993065f21234e681b4c3db270dc174",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.163405109511571,
  "max_drift_m": 2.163405109511571,
  "radial_IAE_m_s": 71.49995765873851,
  "signed_longitudinal_delta_m": 2.154559501370718,
  "tail_speed_mean_m_s": 0.03163251683432635,
  "tail_speed_rms_m_s": 0.03163645378736404,
  "tail_sensor_speed_mean_m_s": 0.031563928969216906,
  "tail_fk_speed_mean_m_s": 0.03156280718944261,
  "peak_tilt_rad": 0.08143312908151379,
  "peak_wheel_torque_nm": 1.524170994758606,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.30977274099132
}
```
