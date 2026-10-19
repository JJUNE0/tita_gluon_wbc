# tita_flash_sac_193248_068255_model_5000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "b60b192b9d2f23858fdffe55ec465d178806e473ef4c4913e439a7ef2e3a0fd4",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.5838068115018606,
  "max_drift_m": 1.7358853251160644,
  "radial_IAE_m_s": 342.8428547278469,
  "signed_longitudinal_delta_m": -0.4557567254463778,
  "tail_speed_mean_m_s": -0.039870263386270005,
  "tail_speed_rms_m_s": 0.03987026374837691,
  "tail_sensor_speed_mean_m_s": -0.04029590082133611,
  "tail_fk_speed_mean_m_s": -0.04066522592996118,
  "peak_tilt_rad": 0.09270502437929373,
  "peak_wheel_torque_nm": 0.8839302062988281,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 45.219990890007466
}
```
