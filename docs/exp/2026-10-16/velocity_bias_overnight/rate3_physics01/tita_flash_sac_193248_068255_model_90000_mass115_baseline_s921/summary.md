# tita_flash_sac_193248_068255_model_90000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "616eaa811511495e3b4a9eb905c85899ff4212dd28e09262a262a7f90e92c8b8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.6880304653418224,
  "max_drift_m": 0.6880304653418224,
  "radial_IAE_m_s": 16.282204452718645,
  "signed_longitudinal_delta_m": 0.6876328430519592,
  "tail_speed_mean_m_s": 0.016177791564398518,
  "tail_speed_rms_m_s": 0.019412866292528256,
  "tail_sensor_speed_mean_m_s": 0.016485488099022227,
  "tail_fk_speed_mean_m_s": 0.01640561290920434,
  "peak_tilt_rad": 0.11697849898495627,
  "peak_wheel_torque_nm": 4.665751934051514,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.550876927038189
}
```
