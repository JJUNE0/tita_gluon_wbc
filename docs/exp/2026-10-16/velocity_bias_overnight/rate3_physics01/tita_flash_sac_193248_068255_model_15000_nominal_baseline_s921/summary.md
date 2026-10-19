# tita_flash_sac_193248_068255_model_15000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "initial_physics_sha256": "0dacc359635104403574016f58cbbaec66e8c59e8929a4243976305907524fa5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.422267111852551,
  "max_drift_m": 3.422267111852551,
  "radial_IAE_m_s": 102.93352229215085,
  "signed_longitudinal_delta_m": -3.422234878406345,
  "tail_speed_mean_m_s": -0.05674225921274661,
  "tail_speed_rms_m_s": 0.056742313379136516,
  "tail_sensor_speed_mean_m_s": -0.05665330500973415,
  "tail_fk_speed_mean_m_s": -0.05665346375122459,
  "peak_tilt_rad": 0.0442409178164731,
  "peak_wheel_torque_nm": 0.07639738917350769,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.41035171103431
}
```
