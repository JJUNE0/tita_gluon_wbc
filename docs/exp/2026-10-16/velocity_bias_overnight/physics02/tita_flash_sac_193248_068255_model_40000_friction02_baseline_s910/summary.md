# tita_flash_sac_193248_068255_model_40000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "initial_physics_sha256": "4b5e043a99525ed2bc070a6a8428b09921510263323de1a79dcc177551f18e0d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.745335018624885,
  "max_drift_m": 10.745335018624885,
  "radial_IAE_m_s": 323.0352972818216,
  "signed_longitudinal_delta_m": 10.590551382082339,
  "tail_speed_mean_m_s": 0.17962321173926474,
  "tail_speed_rms_m_s": 0.17962322967621744,
  "tail_sensor_speed_mean_m_s": 0.1792353008094584,
  "tail_fk_speed_mean_m_s": 0.17922682643236407,
  "peak_tilt_rad": 0.12097519146076485,
  "peak_wheel_torque_nm": 0.12151992321014404,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.840263036021497
}
```
