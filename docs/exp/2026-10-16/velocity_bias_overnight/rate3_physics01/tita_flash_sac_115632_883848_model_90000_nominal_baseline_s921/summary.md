# tita_flash_sac_115632_883848_model_90000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "c2cce1bb62555008a2974f1f1703e0241595a576e5ae6cae629772ee130bb95d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.694947564156429,
  "max_drift_m": 6.694947564156429,
  "radial_IAE_m_s": 198.9964710275854,
  "signed_longitudinal_delta_m": 6.693585455187228,
  "tail_speed_mean_m_s": 0.1133228506911971,
  "tail_speed_rms_m_s": 0.11332312215064201,
  "tail_sensor_speed_mean_m_s": 0.1130775514914094,
  "tail_fk_speed_mean_m_s": 0.1130758283655414,
  "peak_tilt_rad": 0.07073674765070526,
  "peak_wheel_torque_nm": 0.19447940587997437,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.666398219997063
}
```
