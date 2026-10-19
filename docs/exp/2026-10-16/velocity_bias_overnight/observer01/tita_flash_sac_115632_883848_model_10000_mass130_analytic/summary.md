# tita_flash_sac_115632_883848_model_10000_mass130_analytic

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass130_analytic",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "analytic",
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
  "initial_physics_sha256": "71af3ba2abad2c7894490b99eec3c868df9493c641cde1bcb329281cb0731f6c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013347397467395786,
  "max_drift_m": 0.016401537011855632,
  "radial_IAE_m_s": 0.8874258387969116,
  "signed_longitudinal_delta_m": -0.013347060232099325,
  "tail_speed_mean_m_s": 2.0671018813671428e-05,
  "tail_speed_rms_m_s": 0.006494735168902449,
  "tail_sensor_speed_mean_m_s": -1.0839094592541225e-05,
  "tail_fk_speed_mean_m_s": 2.6705989149236144e-05,
  "peak_tilt_rad": 0.0878896016321189,
  "peak_wheel_torque_nm": 0.659509539604187,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12947933134774672,
  "final_integral_m_s": -0.13645597691490996,
  "elapsed_wall_s": 17.835388803971
}
```
