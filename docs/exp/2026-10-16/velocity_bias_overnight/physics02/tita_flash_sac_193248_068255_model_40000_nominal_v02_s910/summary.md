# tita_flash_sac_193248_068255_model_40000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "75d2728b583524348a87a9046bd8a1fb6104ff6934a9ad5aa42219ab2acea2d6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02451372245432777,
  "max_drift_m": 0.04397243360196119,
  "radial_IAE_m_s": 1.421254116395116,
  "signed_longitudinal_delta_m": 0.02451370127382803,
  "tail_speed_mean_m_s": 3.0592805021488884e-05,
  "tail_speed_rms_m_s": 3.0606386966110425e-05,
  "tail_sensor_speed_mean_m_s": 3.089948852517446e-05,
  "tail_fk_speed_mean_m_s": 3.0262828153746805e-05,
  "peak_tilt_rad": 0.10857957817436592,
  "peak_wheel_torque_nm": 0.891409158706665,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2583995269138038,
  "final_integral_m_s": 0.2583375089756712,
  "elapsed_wall_s": 17.591910178016406
}
```
