# tita_flash_sac_193248_068255_model_40000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "45e0be99c57980674f04dc61eda35a09e235ae3f43155c26751cdfd1286a95e8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.355818078690728,
  "max_drift_m": 10.355818078690728,
  "radial_IAE_m_s": 307.18932137766893,
  "signed_longitudinal_delta_m": 10.290095919883626,
  "tail_speed_mean_m_s": 0.17812888067412994,
  "tail_speed_rms_m_s": 0.17812957725000483,
  "tail_sensor_speed_mean_m_s": 0.17774459479288154,
  "tail_fk_speed_mean_m_s": 0.17773559685840612,
  "peak_tilt_rad": 0.13587308611346938,
  "peak_wheel_torque_nm": 1.2942160367965698,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.740561606944539
}
```
