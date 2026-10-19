# tita_flash_sac_193248_068255_model_40000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "717b2c3a600437e3ea4d0dd957db5794146b6a7b2be84ec7ed80adb093099917",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.01941986861228,
  "max_drift_m": 10.01941986861228,
  "radial_IAE_m_s": 289.13380460510496,
  "signed_longitudinal_delta_m": 9.989467837073017,
  "tail_speed_mean_m_s": 0.17772619973856127,
  "tail_speed_rms_m_s": 0.17772740085144056,
  "tail_sensor_speed_mean_m_s": 0.17734288936744813,
  "tail_fk_speed_mean_m_s": 0.17733375313735486,
  "peak_tilt_rad": 0.12023550501287339,
  "peak_wheel_torque_nm": 0.13283824920654297,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.986766204005107
}
```
