# tita_flash_sac_115632_883848_model_80000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "8d160aa7395d03deeec143ce54d389a51b57d38fc4d3e68ab5b14fe3d9ea5c81",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.08873549831654241,
  "max_drift_m": 0.089216902853357,
  "radial_IAE_m_s": 25.445347227457727,
  "signed_longitudinal_delta_m": 0.08833620931255567,
  "tail_speed_mean_m_s": 5.386629031848502e-06,
  "tail_speed_rms_m_s": 5.390499382577168e-06,
  "tail_sensor_speed_mean_m_s": 4.525641317885233e-06,
  "tail_fk_speed_mean_m_s": 3.397857127120225e-07,
  "peak_tilt_rad": 0.0842946438772243,
  "peak_wheel_torque_nm": 0.6498018503189087,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.9159469583879463,
  "final_integral_m_s": 0.915946711833689,
  "elapsed_wall_s": 67.93056625698227
}
```
