# tita_flash_sac_193248_068255_model_40000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "f202866fdac727327eec64f268fc987a62083e3837bd1c6d16aea5332fd53713",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.868800474960283,
  "max_drift_m": 9.868800474960283,
  "radial_IAE_m_s": 279.6275694363544,
  "signed_longitudinal_delta_m": 9.811663059693258,
  "tail_speed_mean_m_s": 0.17784710704866755,
  "tail_speed_rms_m_s": 0.1778481445733557,
  "tail_sensor_speed_mean_m_s": 0.1774634993981858,
  "tail_fk_speed_mean_m_s": 0.1774544091300076,
  "peak_tilt_rad": 0.1202448070428288,
  "peak_wheel_torque_nm": 1.4816185235977173,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.992396446992643
}
```
