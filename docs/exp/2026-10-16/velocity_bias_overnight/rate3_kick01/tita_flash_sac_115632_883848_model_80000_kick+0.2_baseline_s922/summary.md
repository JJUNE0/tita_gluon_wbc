# tita_flash_sac_115632_883848_model_80000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "238b9e04d9a487ecd84a40a886f1f7227aa8238dcc7bc9dccc398dece1d6da7a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.863994124548311,
  "max_drift_m": 11.863994124548311,
  "radial_IAE_m_s": 354.97623253818284,
  "signed_longitudinal_delta_m": 11.825859593716388,
  "tail_speed_mean_m_s": 0.19958943209294866,
  "tail_speed_rms_m_s": 0.199589689092006,
  "tail_sensor_speed_mean_m_s": 0.19915829552919506,
  "tail_fk_speed_mean_m_s": 0.1991573319296,
  "peak_tilt_rad": 0.1032425898904028,
  "peak_wheel_torque_nm": 1.9176570177078247,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.413747097016312
}
```
