# tita_flash_sac_193248_068255_model_15000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "initial_physics_sha256": "49f56fcec3b2ef515a8de6bc5c71f26d25ca28e3b9d5dea7f12b6bfcedde7376",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.5589326856717207,
  "max_drift_m": 2.5589326856717207,
  "radial_IAE_m_s": 76.89482309870758,
  "signed_longitudinal_delta_m": -2.557861512745664,
  "tail_speed_mean_m_s": -0.04251163242447483,
  "tail_speed_rms_m_s": 0.04251165711105613,
  "tail_sensor_speed_mean_m_s": -0.04243981848737375,
  "tail_fk_speed_mean_m_s": -0.04243794206289157,
  "peak_tilt_rad": 0.04828029947162382,
  "peak_wheel_torque_nm": 0.07585795223712921,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.642798380984459
}
```
