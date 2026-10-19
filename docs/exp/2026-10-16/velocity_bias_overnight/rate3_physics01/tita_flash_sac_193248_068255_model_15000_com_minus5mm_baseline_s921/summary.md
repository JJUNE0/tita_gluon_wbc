# tita_flash_sac_193248_068255_model_15000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "9c5d92119d2a3972bdd0724ff098877afcef445fc4195ee93c0b23a084eb96fb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.394041153980419,
  "max_drift_m": 4.394041153980419,
  "radial_IAE_m_s": 131.88412217686562,
  "signed_longitudinal_delta_m": -4.393828379207116,
  "tail_speed_mean_m_s": -0.07319479494411324,
  "tail_speed_rms_m_s": 0.07319479760845647,
  "tail_sensor_speed_mean_m_s": -0.07308063765001681,
  "tail_fk_speed_mean_m_s": -0.07308282557141611,
  "peak_tilt_rad": 0.04001665145214961,
  "peak_wheel_torque_nm": 0.09275570511817932,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.755676699976902
}
```
