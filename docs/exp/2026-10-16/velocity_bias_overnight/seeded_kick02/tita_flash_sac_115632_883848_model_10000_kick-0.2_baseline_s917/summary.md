# tita_flash_sac_115632_883848_model_10000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "f3fff3e7f1bf2bb7742af9657e24be3214ff920ec427deee16dcb21a1c81128d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.3663958888207204,
  "max_drift_m": 1.3663958888207204,
  "radial_IAE_m_s": 40.98748019916771,
  "signed_longitudinal_delta_m": 1.3656787854733876,
  "tail_speed_mean_m_s": 0.022018351452899432,
  "tail_speed_rms_m_s": 0.024337566175730352,
  "tail_sensor_speed_mean_m_s": 0.020048613771283013,
  "tail_fk_speed_mean_m_s": 0.02185937614210041,
  "peak_tilt_rad": 0.11311485804301347,
  "peak_wheel_torque_nm": 3.249549627304077,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.237814317981247
}
```
