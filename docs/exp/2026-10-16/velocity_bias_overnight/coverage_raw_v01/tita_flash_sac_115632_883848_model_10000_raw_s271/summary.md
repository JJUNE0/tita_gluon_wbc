# tita_flash_sac_115632_883848_model_10000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "a86667a6cf17e0bab6a9b790fff3b087f730a312547a7ba5416973ebcbd8da07",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004230478348194275,
  "max_drift_m": 0.03162404326923002,
  "radial_IAE_m_s": 0.5630697207941142,
  "signed_longitudinal_delta_m": 0.004054924971910031,
  "tail_speed_mean_m_s": 0.00017150583747926174,
  "tail_speed_rms_m_s": 0.036140171897018486,
  "tail_sensor_speed_mean_m_s": 0.002984958555870222,
  "tail_fk_speed_mean_m_s": 0.00035435062262674196,
  "peak_tilt_rad": 0.12777737766147368,
  "peak_wheel_torque_nm": 3.3446543216705322,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2501960111713093,
  "final_integral_m_s": 0.14656963928206598,
  "elapsed_wall_s": 4.903390650055371
}
```
