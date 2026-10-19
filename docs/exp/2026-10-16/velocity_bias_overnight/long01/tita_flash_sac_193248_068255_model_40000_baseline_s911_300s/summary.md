# tita_flash_sac_193248_068255_model_40000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "4cb502b3767ae39fbd598ac138086f205efc5ed3e828c6110f22c1aa35e979b9",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 47.24358315012484,
  "max_drift_m": 47.24358315012484,
  "radial_IAE_m_s": 7456.321571007984,
  "signed_longitudinal_delta_m": 33.40694573744997,
  "tail_speed_mean_m_s": 0.17941080831629186,
  "tail_speed_rms_m_s": 0.17941080831684472,
  "tail_sensor_speed_mean_m_s": 0.179023418187375,
  "tail_fk_speed_mean_m_s": 0.17901486521373644,
  "peak_tilt_rad": 0.12036519538149237,
  "peak_wheel_torque_nm": 0.13322395086288452,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 57.09789243695559
}
```
