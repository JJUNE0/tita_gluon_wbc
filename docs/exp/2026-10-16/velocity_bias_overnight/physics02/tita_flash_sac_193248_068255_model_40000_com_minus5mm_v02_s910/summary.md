# tita_flash_sac_193248_068255_model_40000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "d4bc312e6b7f3673adb87cd1ab0e02f4dd605b19c97dfebeeaf55e0e3671b341",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020298570001503993,
  "max_drift_m": 0.030829914486823012,
  "radial_IAE_m_s": 1.1518242718186453,
  "signed_longitudinal_delta_m": 0.02029827545683026,
  "tail_speed_mean_m_s": 3.971372097731359e-05,
  "tail_speed_rms_m_s": 3.973218170780448e-05,
  "tail_sensor_speed_mean_m_s": 3.99950893398751e-05,
  "tail_fk_speed_mean_m_s": 3.9368176215841635e-05,
  "peak_tilt_rad": 0.10087116882362102,
  "peak_wheel_torque_nm": 0.6091493368148804,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.21177986995662312,
  "final_integral_m_s": 0.2117044536569173,
  "elapsed_wall_s": 15.439777557970956
}
```
