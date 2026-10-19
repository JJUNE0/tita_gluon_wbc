# tita_flash_sac_193248_068255_model_90000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "initial_physics_sha256": "b147b85f181a4707ef4048fe5e23c84329796bdd21813313fcfbf23bc295424b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.899170398215393,
  "max_drift_m": 15.899170398215393,
  "radial_IAE_m_s": 468.04909551478795,
  "signed_longitudinal_delta_m": 15.888677149216097,
  "tail_speed_mean_m_s": 0.27206025025174363,
  "tail_speed_rms_m_s": 0.27206029603200854,
  "tail_sensor_speed_mean_m_s": 0.271471608224429,
  "tail_fk_speed_mean_m_s": 0.2714694474443143,
  "peak_tilt_rad": 0.1179457165993929,
  "peak_wheel_torque_nm": 1.9495900869369507,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.60720006399788
}
```
