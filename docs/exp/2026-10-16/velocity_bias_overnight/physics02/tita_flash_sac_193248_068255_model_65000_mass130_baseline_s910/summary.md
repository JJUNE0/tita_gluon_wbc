# tita_flash_sac_193248_068255_model_65000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "a78864b3a81899d2cc35b1666eee42dc7017e4b0b532d082a8a12c602d0f8a29",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.943935049305956,
  "max_drift_m": 11.943935049305956,
  "radial_IAE_m_s": 358.15436241011093,
  "signed_longitudinal_delta_m": -11.827666609363988,
  "tail_speed_mean_m_s": -0.20019219208864322,
  "tail_speed_rms_m_s": 0.2001922056366096,
  "tail_sensor_speed_mean_m_s": -0.1997730623234344,
  "tail_fk_speed_mean_m_s": -0.1997694444831995,
  "peak_tilt_rad": 0.03114102688113629,
  "peak_wheel_torque_nm": 0.29543161392211914,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.36976194701856
}
```
