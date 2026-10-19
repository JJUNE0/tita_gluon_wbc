# tita_flash_sac_193248_068255_model_5000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "fb9f5e99a3e3fb72fad7315b30d63f21f6d5a113ebd87ef2b9f913908c755235",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.4884542187860285,
  "max_drift_m": 1.6980858788261695,
  "radial_IAE_m_s": 69.56262831467018,
  "signed_longitudinal_delta_m": 0.43580022584732464,
  "tail_speed_mean_m_s": -0.07889875503643953,
  "tail_speed_rms_m_s": 0.07891038722126847,
  "tail_sensor_speed_mean_m_s": -0.07793603539898757,
  "tail_fk_speed_mean_m_s": -0.07848830524999229,
  "peak_tilt_rad": 0.06964071920398651,
  "peak_wheel_torque_nm": 0.08223280310630798,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.74440256995149
}
```
