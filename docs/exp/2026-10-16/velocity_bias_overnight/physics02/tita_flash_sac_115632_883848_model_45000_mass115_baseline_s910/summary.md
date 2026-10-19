# tita_flash_sac_115632_883848_model_45000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "1922518b778d887b47e3d71bd87e32f95959710f2883fe83ee57ac9eb960dec1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.985340987485187,
  "max_drift_m": 4.985340987485187,
  "radial_IAE_m_s": 148.25153574121165,
  "signed_longitudinal_delta_m": -4.939961599211328,
  "tail_speed_mean_m_s": -0.08495237554951626,
  "tail_speed_rms_m_s": 0.08495365133036951,
  "tail_sensor_speed_mean_m_s": -0.08476904117158819,
  "tail_fk_speed_mean_m_s": -0.08476678329455072,
  "peak_tilt_rad": 0.022226978517968954,
  "peak_wheel_torque_nm": 1.1409894227981567,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.514267626975197
}
```
