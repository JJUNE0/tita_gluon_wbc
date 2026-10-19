# tita_flash_sac_115632_883848_model_65000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
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
  "initial_physics_sha256": "f4d6c3ddede1dbe3112f9c969a3a10a45b61d9a35fa847ea3835f103cb15bf97",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.1711644093298244,
  "max_drift_m": 2.1711644093298244,
  "radial_IAE_m_s": 71.73483918871511,
  "signed_longitudinal_delta_m": 2.1620116758626517,
  "tail_speed_mean_m_s": 0.03176827501698556,
  "tail_speed_rms_m_s": 0.03177220022677964,
  "tail_sensor_speed_mean_m_s": 0.031699415045267264,
  "tail_fk_speed_mean_m_s": 0.03169829874144859,
  "peak_tilt_rad": 0.08148282917054939,
  "peak_wheel_torque_nm": 1.524119257926941,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.834710761031602
}
```
