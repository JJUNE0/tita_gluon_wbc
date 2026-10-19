# tita_flash_sac_115632_883848_model_45000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "1ab81ae85b0e79baf7effd0ebaf356b67bcfa5c9fe333ab1903caabdeda01646",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03590940296915835,
  "max_drift_m": 0.06129103288911189,
  "radial_IAE_m_s": 2.171348468827147,
  "signed_longitudinal_delta_m": 0.035905371337078995,
  "tail_speed_mean_m_s": -4.4186784950602246e-05,
  "tail_speed_rms_m_s": 4.468253277934963e-05,
  "tail_sensor_speed_mean_m_s": -4.372394828583848e-05,
  "tail_fk_speed_mean_m_s": -4.166076771279782e-05,
  "peak_tilt_rad": 0.15434152429870185,
  "peak_wheel_torque_nm": 6.978832721710205,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3509676987423667,
  "final_integral_m_s": -0.3509676987423667,
  "elapsed_wall_s": 6.589843583991751
}
```
