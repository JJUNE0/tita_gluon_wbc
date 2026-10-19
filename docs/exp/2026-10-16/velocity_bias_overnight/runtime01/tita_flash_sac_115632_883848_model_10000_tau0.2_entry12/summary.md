# tita_flash_sac_115632_883848_model_10000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "initial_physics_sha256": "d3c9a9fd9be982eaafef6a684cae968e0664cdaf0451f3b9d510f9102c1aa3a0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03569028096817881,
  "max_drift_m": 0.04215147873088414,
  "radial_IAE_m_s": 2.0561924214665592,
  "signed_longitudinal_delta_m": 0.035662683220665646,
  "tail_speed_mean_m_s": 1.761475177587481e-05,
  "tail_speed_rms_m_s": 0.01688289118046383,
  "tail_sensor_speed_mean_m_s": -1.2806919494757906e-05,
  "tail_fk_speed_mean_m_s": -6.247055208137903e-05,
  "peak_tilt_rad": 0.11399445229705307,
  "peak_wheel_torque_nm": 2.907289743423462,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3119911894515169,
  "final_integral_m_s": 0.3078496948289709,
  "elapsed_wall_s": 6.5337083989870735
}
```
