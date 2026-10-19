# tita_flash_sac_193248_068255_model_40000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "a14ad0a80722b63699dea58922103c5c41a2dacc2819f782ff3a2878b6949810",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.18167986184227,
  "max_drift_m": 12.18167986184227,
  "radial_IAE_m_s": 358.9215500009983,
  "signed_longitudinal_delta_m": 12.062385864980133,
  "tail_speed_mean_m_s": 0.2097446364530229,
  "tail_speed_rms_m_s": 0.20974475700441012,
  "tail_sensor_speed_mean_m_s": 0.20929179011821017,
  "tail_fk_speed_mean_m_s": 0.20928333418781764,
  "peak_tilt_rad": 0.1260318447829849,
  "peak_wheel_torque_nm": 0.1416536569595337,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.57808228500653
}
```
