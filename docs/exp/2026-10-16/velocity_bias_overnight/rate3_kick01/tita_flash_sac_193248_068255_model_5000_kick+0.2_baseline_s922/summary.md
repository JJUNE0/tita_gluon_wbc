# tita_flash_sac_193248_068255_model_5000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "33ec78484ee52f8a046f5973ee46acd532bc6e9ca472ef0a163991665072cee8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.4837315992669255,
  "max_drift_m": 1.6215184103322933,
  "radial_IAE_m_s": 67.77417817322811,
  "signed_longitudinal_delta_m": -0.11326630338209558,
  "tail_speed_mean_m_s": -0.044626134605088096,
  "tail_speed_rms_m_s": 0.04463850008095368,
  "tail_sensor_speed_mean_m_s": -0.045230395393887984,
  "tail_fk_speed_mean_m_s": -0.04559152012340631,
  "peak_tilt_rad": 0.0889627355974123,
  "peak_wheel_torque_nm": 4.642065525054932,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.501340062008239
}
```
