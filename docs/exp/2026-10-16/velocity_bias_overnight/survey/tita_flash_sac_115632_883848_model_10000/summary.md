# tita_flash_sac_115632_883848_model_10000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "bf080e1af8d81415dd8ed6ce0ebb3c84ef64c0f48255e0341db61c52c1209bf8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.382424121607864,
  "max_drift_m": 1.382424121607864,
  "radial_IAE_m_s": 42.79875069910378,
  "signed_longitudinal_delta_m": 1.38200824183281,
  "tail_speed_mean_m_s": 0.021626166010567473,
  "tail_speed_rms_m_s": 0.023963897573379984,
  "tail_sensor_speed_mean_m_s": 0.02215633442355421,
  "tail_fk_speed_mean_m_s": 0.021612655169171893,
  "peak_tilt_rad": 0.11310312342673634,
  "peak_wheel_torque_nm": 2.842339038848877,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.757343154982664
}
```
