# tita_flash_sac_193248_068255_model_90000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "e288b08d7f69eb87824f4faa27030142339845478ed0eb3331c4790ef1292c4e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.912333235736462,
  "max_drift_m": 12.912333235736462,
  "radial_IAE_m_s": 377.28666784875907,
  "signed_longitudinal_delta_m": 12.798146720837535,
  "tail_speed_mean_m_s": 0.223305613656077,
  "tail_speed_rms_m_s": 0.22330586166619765,
  "tail_sensor_speed_mean_m_s": 0.22283629278735784,
  "tail_fk_speed_mean_m_s": 0.22283428242126013,
  "peak_tilt_rad": 0.11193842790528219,
  "peak_wheel_torque_nm": 0.9037437438964844,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.71857462101616
}
```
