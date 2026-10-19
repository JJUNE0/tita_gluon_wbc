# tita_flash_sac_193248_068255_model_65000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "e063059cbd6f8b8cb00fd9e3ee403e7d82f81c1733f92008accb4f341269f12c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.696781504824374,
  "max_drift_m": 4.696781504824374,
  "radial_IAE_m_s": 140.8211531303274,
  "signed_longitudinal_delta_m": -4.696335030816498,
  "tail_speed_mean_m_s": -0.07819569375490222,
  "tail_speed_rms_m_s": 0.07819574478635134,
  "tail_sensor_speed_mean_m_s": -0.07806835314565941,
  "tail_fk_speed_mean_m_s": -0.07806653797831899,
  "peak_tilt_rad": 0.025259557763243068,
  "peak_wheel_torque_nm": 0.05867168307304382,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.341061332030222
}
```
