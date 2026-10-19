# tita_flash_sac_115632_883848_model_45000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "0dbeb4d10415a9cd96743c9aaacd502177d49c703918042221b66b720844ee0b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.7131303295611104,
  "max_drift_m": 2.7131303295611104,
  "radial_IAE_m_s": 80.6743233128829,
  "signed_longitudinal_delta_m": 2.6478556615797566,
  "tail_speed_mean_m_s": 0.04605077805526951,
  "tail_speed_rms_m_s": 0.04662418764247559,
  "tail_sensor_speed_mean_m_s": 0.04619316568148499,
  "tail_fk_speed_mean_m_s": 0.046069271442642806,
  "peak_tilt_rad": 0.05208714958314564,
  "peak_wheel_torque_nm": 2.6125574111938477,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.402306011004839
}
```
