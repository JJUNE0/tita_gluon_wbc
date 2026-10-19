# tita_flash_sac_193248_068255_model_40000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "initial_physics_sha256": "38be0eb9e53eb8542cbbcbcec85ce266cf32c062fa4f70a31730348c3c59949c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.745327710141002,
  "max_drift_m": 10.745327710141002,
  "radial_IAE_m_s": 323.0349614414523,
  "signed_longitudinal_delta_m": 10.590543252957952,
  "tail_speed_mean_m_s": 0.17962318902272995,
  "tail_speed_rms_m_s": 0.17962320695427925,
  "tail_sensor_speed_mean_m_s": 0.1792352788607342,
  "tail_fk_speed_mean_m_s": 0.17922680420481288,
  "peak_tilt_rad": 0.12097513051206521,
  "peak_wheel_torque_nm": 0.12152141332626343,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.078829851001501
}
```
