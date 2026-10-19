# tita_flash_sac_115632_883848_model_45000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "a906f6ed99fd7c86d9b067011da14ab7cb299a477fc56917441320bbcb9d4511",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.387751113528026,
  "max_drift_m": 2.387751113528026,
  "radial_IAE_m_s": 68.0821601154653,
  "signed_longitudinal_delta_m": 2.3184867948531185,
  "tail_speed_mean_m_s": 0.042348365722639225,
  "tail_speed_rms_m_s": 0.04295151202331739,
  "tail_sensor_speed_mean_m_s": 0.04114121092020255,
  "tail_fk_speed_mean_m_s": 0.04224253852208626,
  "peak_tilt_rad": 0.05224231666607149,
  "peak_wheel_torque_nm": 2.7568681240081787,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.248519522952847
}
```
