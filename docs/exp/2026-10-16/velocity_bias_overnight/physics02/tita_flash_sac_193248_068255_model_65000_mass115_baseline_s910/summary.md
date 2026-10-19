# tita_flash_sac_193248_068255_model_65000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "4d46e12f43d48925f1644d421611753b759d88d6a796434439d63fc234f9a56b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.646111149073936,
  "max_drift_m": 7.646111149073936,
  "radial_IAE_m_s": 229.40176796698927,
  "signed_longitudinal_delta_m": -7.615606461486176,
  "tail_speed_mean_m_s": -0.12761393580669056,
  "tail_speed_rms_m_s": 0.12761394967648826,
  "tail_sensor_speed_mean_m_s": -0.12736312059127955,
  "tail_fk_speed_mean_m_s": -0.12735727574092612,
  "peak_tilt_rad": 0.02590057924387712,
  "peak_wheel_torque_nm": 0.09066367149353027,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.46897547703702
}
```
