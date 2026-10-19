# tita_flash_sac_193248_068255_model_40000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "d4bc312e6b7f3673adb87cd1ab0e02f4dd605b19c97dfebeeaf55e0e3671b341",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.916836674383133,
  "max_drift_m": 7.916836674383133,
  "radial_IAE_m_s": 226.23913104707114,
  "signed_longitudinal_delta_m": 7.8855295820009506,
  "tail_speed_mean_m_s": 0.14254949366893957,
  "tail_speed_rms_m_s": 0.14255327258339542,
  "tail_sensor_speed_mean_m_s": 0.14224233884039625,
  "tail_fk_speed_mean_m_s": 0.14223379418080498,
  "peak_tilt_rad": 0.11322918726936959,
  "peak_wheel_torque_nm": 0.11351418495178223,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.47834467102075
}
```
