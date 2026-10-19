# tita_flash_sac_115632_883848_model_45000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "40fa3c2a6d62c955d11029b10da806474269ff6f0d8d7c39dcb9591c99d3a06a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.24835129019619,
  "max_drift_m": 2.24835129019619,
  "radial_IAE_m_s": 66.07621994537388,
  "signed_longitudinal_delta_m": 2.185879202623383,
  "tail_speed_mean_m_s": 0.03887624485063325,
  "tail_speed_rms_m_s": 0.03945264426460073,
  "tail_sensor_speed_mean_m_s": 0.03834809070940216,
  "tail_fk_speed_mean_m_s": 0.03887039267508683,
  "peak_tilt_rad": 0.051683355358490335,
  "peak_wheel_torque_nm": 2.7709062099456787,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.270824713050388
}
```
