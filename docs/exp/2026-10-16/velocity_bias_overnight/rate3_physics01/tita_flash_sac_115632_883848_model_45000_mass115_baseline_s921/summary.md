# tita_flash_sac_115632_883848_model_45000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "7ba11da4026719344e6f4c9931234a60aa4fa446321c9dcfe06597734a3af55e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.958496422190972,
  "max_drift_m": 4.958496422190972,
  "radial_IAE_m_s": 147.52006698759226,
  "signed_longitudinal_delta_m": -4.908267774038108,
  "tail_speed_mean_m_s": -0.08442019060905617,
  "tail_speed_rms_m_s": 0.08442176481555687,
  "tail_sensor_speed_mean_m_s": -0.0842378514880864,
  "tail_fk_speed_mean_m_s": -0.08423574533127005,
  "peak_tilt_rad": 0.02248815629534029,
  "peak_wheel_torque_nm": 1.1356041431427002,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.673831144988071
}
```
