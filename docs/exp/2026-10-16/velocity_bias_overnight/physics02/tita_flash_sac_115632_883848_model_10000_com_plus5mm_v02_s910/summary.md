# tita_flash_sac_115632_883848_model_10000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "final_drift_m": 0.03863740009785788,
  "max_drift_m": 0.041640958357406395,
  "radial_IAE_m_s": 2.2193041314778865,
  "signed_longitudinal_delta_m": 0.03859654034475129,
  "tail_speed_mean_m_s": -0.00011120036448755416,
  "tail_speed_rms_m_s": 0.022421803276176704,
  "tail_sensor_speed_mean_m_s": -0.0024104519005783156,
  "tail_fk_speed_mean_m_s": -0.0002449802717119565,
  "peak_tilt_rad": 0.11747657931265665,
  "peak_wheel_torque_nm": 3.085876941680908,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3107373703857678,
  "final_integral_m_s": 0.345444225597591,
  "elapsed_wall_s": 20.896752098982688
}
```
