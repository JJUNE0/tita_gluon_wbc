# tita_flash_sac_115632_883848_model_10000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "2319166af7245a16161dc0df7e2e9e9eba15b0ebe18680aabad41fdfeaa3fc29",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.9762795804101356,
  "max_drift_m": 1.9762795804101356,
  "radial_IAE_m_s": 60.775067582492355,
  "signed_longitudinal_delta_m": 1.9750670403312296,
  "tail_speed_mean_m_s": 0.031406232807803414,
  "tail_speed_rms_m_s": 0.03425356900234824,
  "tail_sensor_speed_mean_m_s": 0.03130404621991183,
  "tail_fk_speed_mean_m_s": 0.031157389256726377,
  "peak_tilt_rad": 0.12055409207695544,
  "peak_wheel_torque_nm": 3.1317496299743652,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.132149312004913
}
```
