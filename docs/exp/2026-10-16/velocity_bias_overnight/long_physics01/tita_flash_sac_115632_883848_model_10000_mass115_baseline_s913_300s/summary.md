# tita_flash_sac_115632_883848_model_10000_mass115_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass115_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "6cc905a1c989323cd4ca841dd842f21344432b7fa44e860c3a54ca96474997c9",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 10.4655261946988,
  "max_drift_m": 10.4655261946988,
  "radial_IAE_m_s": 1583.459099020833,
  "signed_longitudinal_delta_m": -9.820923041661947,
  "tail_speed_mean_m_s": -0.03635725877707027,
  "tail_speed_rms_m_s": 0.05219613099319542,
  "tail_sensor_speed_mean_m_s": -0.038810724190796016,
  "tail_fk_speed_mean_m_s": -0.03613529415362943,
  "peak_tilt_rad": 0.11710114728844245,
  "peak_wheel_torque_nm": 4.844752311706543,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 66.8855322249583
}
```
