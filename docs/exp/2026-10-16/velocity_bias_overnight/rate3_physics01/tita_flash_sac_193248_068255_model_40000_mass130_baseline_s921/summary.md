# tita_flash_sac_193248_068255_model_40000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "bc5cfaf4197f1bf58ed0e74ab644d2d398dd3aaa368bf241de63e08d7ca5336a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.091501139674802,
  "max_drift_m": 4.091501139674802,
  "radial_IAE_m_s": 122.5590630830203,
  "signed_longitudinal_delta_m": -4.090543365027236,
  "tail_speed_mean_m_s": -0.06821380309097747,
  "tail_speed_rms_m_s": 0.068213840441961,
  "tail_sensor_speed_mean_m_s": -0.0680674123480906,
  "tail_fk_speed_mean_m_s": -0.06806694220939793,
  "peak_tilt_rad": 0.11717383659436753,
  "peak_wheel_torque_nm": 0.2907561659812927,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.093840686953627
}
```
