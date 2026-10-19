# tita_flash_sac_115632_883848_model_10000_friction08_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_friction08_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "f161ff51b00b3adbc063135bb61b363f579c6fc84619ebbd5fe2ca62c4ca1f34",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 6.296783177932659,
  "max_drift_m": 6.296783177932659,
  "radial_IAE_m_s": 981.8977857403484,
  "signed_longitudinal_delta_m": 6.257256150471571,
  "tail_speed_mean_m_s": 0.019973073240459084,
  "tail_speed_rms_m_s": 0.022348101048162625,
  "tail_sensor_speed_mean_m_s": 0.019860893123090213,
  "tail_fk_speed_mean_m_s": 0.01970119140521164,
  "peak_tilt_rad": 0.11507741024252982,
  "peak_wheel_torque_nm": 2.840893268585205,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 44.68597901798785
}
```
