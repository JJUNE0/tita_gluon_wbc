# tita_flash_sac_193248_068255_model_10000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
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
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "587f1c3a07adbc5b3dce3ad9194495f510fa399ff4f33aece37fd4978112a55d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.0809668743047944,
  "max_drift_m": 1.0809668743047944,
  "radial_IAE_m_s": 41.794385943740494,
  "signed_longitudinal_delta_m": 0.04129827455973929,
  "tail_speed_mean_m_s": 0.026584349410581774,
  "tail_speed_rms_m_s": 0.026584349440334023,
  "tail_sensor_speed_mean_m_s": 0.026734874034198584,
  "tail_fk_speed_mean_m_s": 0.026802161669744202,
  "peak_tilt_rad": 0.018414125218550792,
  "peak_wheel_torque_nm": 0.5801026225090027,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.335755578998942
}
```
