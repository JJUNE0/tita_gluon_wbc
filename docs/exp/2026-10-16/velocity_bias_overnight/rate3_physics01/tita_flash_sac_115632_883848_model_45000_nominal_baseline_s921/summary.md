# tita_flash_sac_115632_883848_model_45000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
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
  "initial_physics_sha256": "032c3054a472066fd06defd06e1ad8be64cb9562a114842bdee9a6bb0c1abf2e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.4698312929573754,
  "max_drift_m": 2.4698312929573754,
  "radial_IAE_m_s": 72.98640249456709,
  "signed_longitudinal_delta_m": 2.4041026818924953,
  "tail_speed_mean_m_s": 0.04231227278420037,
  "tail_speed_rms_m_s": 0.04292026869886517,
  "tail_sensor_speed_mean_m_s": 0.041696314048079004,
  "tail_fk_speed_mean_m_s": 0.04243966707112861,
  "peak_tilt_rad": 0.052152729424629785,
  "peak_wheel_torque_nm": 2.7017695903778076,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.007024192018434
}
```
