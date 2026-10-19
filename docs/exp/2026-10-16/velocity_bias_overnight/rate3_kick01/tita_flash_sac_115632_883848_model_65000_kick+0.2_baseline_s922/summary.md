# tita_flash_sac_115632_883848_model_65000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "a62883d328feb4edc3ea2beda78f90b3a4ec388694b3e207706981126bc04d48",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.163404567934511,
  "max_drift_m": 2.163404567934511,
  "radial_IAE_m_s": 71.49993402164192,
  "signed_longitudinal_delta_m": 2.1545589507774556,
  "tail_speed_mean_m_s": 0.0316325141063041,
  "tail_speed_rms_m_s": 0.03163645108439893,
  "tail_sensor_speed_mean_m_s": 0.03156392602022309,
  "tail_fk_speed_mean_m_s": 0.031562804389828156,
  "peak_tilt_rad": 0.08143316997190131,
  "peak_wheel_torque_nm": 1.5241702795028687,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.592975198989734
}
```
