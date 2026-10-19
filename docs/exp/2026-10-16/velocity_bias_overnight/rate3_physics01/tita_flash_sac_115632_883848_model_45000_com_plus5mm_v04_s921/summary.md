# tita_flash_sac_115632_883848_model_45000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "final_drift_m": 0.0025797709570692527,
  "max_drift_m": 0.01504405518212179,
  "radial_IAE_m_s": 0.24982123507122234,
  "signed_longitudinal_delta_m": 0.0019692060371617956,
  "tail_speed_mean_m_s": -0.00010955188447604063,
  "tail_speed_rms_m_s": 0.007571689299388516,
  "tail_sensor_speed_mean_m_s": 0.0004083496021733502,
  "tail_fk_speed_mean_m_s": 0.00014454554111406203,
  "peak_tilt_rad": 0.04070594678612216,
  "peak_wheel_torque_nm": 2.5412402153015137,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.16531032920183766,
  "final_integral_m_s": 0.16531032920183766,
  "elapsed_wall_s": 7.14544955897145
}
```
