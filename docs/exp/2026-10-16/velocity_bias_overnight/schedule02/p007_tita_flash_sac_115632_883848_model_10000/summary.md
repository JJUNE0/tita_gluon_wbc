# p007_tita_flash_sac_115632_883848_model_10000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p007_tita_flash_sac_115632_883848_model_10000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "gain_velocity": 0.1,
      "gain_tau": 0.3,
      "gain_floor": 0.25
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
  "initial_physics_sha256": "fbf923f95bdae04e5dc4d5798c4a53b03a4e9af4afaf8f4e506ae6e1ee828e9f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0070141134774703625,
  "max_drift_m": 0.041935131063467565,
  "radial_IAE_m_s": 0.7524526173969033,
  "signed_longitudinal_delta_m": -0.006762067373270218,
  "tail_speed_mean_m_s": 0.00014075558264376025,
  "tail_speed_rms_m_s": 0.0001407776535419679,
  "tail_sensor_speed_mean_m_s": 0.0001404938501661354,
  "tail_fk_speed_mean_m_s": 0.00014011125327504978,
  "peak_tilt_rad": 0.11536815670418221,
  "peak_wheel_torque_nm": 2.5091922283172607,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1505064049520146,
  "final_integral_m_s": -0.1505787475396753,
  "elapsed_wall_s": 12.861086434975732
}
```
