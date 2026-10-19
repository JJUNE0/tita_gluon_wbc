# tita_flash_sac_193248_068255_model_15000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "d751ef234843ad916062959da3627b67a9fdfb4ed39f81ac3f60dc267d83a69b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.7974456682786615,
  "max_drift_m": 4.7974456682786615,
  "radial_IAE_m_s": 143.31432795383267,
  "signed_longitudinal_delta_m": -4.795565197661914,
  "tail_speed_mean_m_s": -0.08030090544335676,
  "tail_speed_rms_m_s": 0.08067314431090566,
  "tail_sensor_speed_mean_m_s": -0.08022969077980109,
  "tail_fk_speed_mean_m_s": -0.08007808917843114,
  "peak_tilt_rad": 0.10210452678323367,
  "peak_wheel_torque_nm": 2.2595136165618896,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.80414511600975
}
```
