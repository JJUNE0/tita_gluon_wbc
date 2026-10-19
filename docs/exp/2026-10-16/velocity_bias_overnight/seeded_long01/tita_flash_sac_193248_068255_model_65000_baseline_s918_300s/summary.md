# tita_flash_sac_193248_068255_model_65000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "1e74c6c3a68aee300ca75360d8a2240d8d5a23121f2febdab5ddc68677551f26",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 11.887078496319967,
  "max_drift_m": 11.887078496319967,
  "radial_IAE_m_s": 1859.9697280106511,
  "signed_longitudinal_delta_m": -11.30927946845259,
  "tail_speed_mean_m_s": -0.03769596380242676,
  "tail_speed_rms_m_s": 0.03769602837738316,
  "tail_sensor_speed_mean_m_s": -0.03761433175824642,
  "tail_fk_speed_mean_m_s": -0.03760977817459438,
  "peak_tilt_rad": 0.02953923881627074,
  "peak_wheel_torque_nm": 0.04987715184688568,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 27.18799541401677
}
```
