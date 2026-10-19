# tita_flash_sac_115632_883848_model_10000_mass130_b+0.030

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass130_b+0.030",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 120.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.03,
      "limit": 2.0,
      "slew": 2.0,
      "ramp": 0.25
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
  "duration_s": 120.0,
  "final_drift_m": 3.338210037333592,
  "max_drift_m": 3.338210037333592,
  "radial_IAE_m_s": 208.3396373919603,
  "signed_longitudinal_delta_m": -3.3381932641563274,
  "tail_speed_mean_m_s": -0.024814719715270155,
  "tail_speed_rms_m_s": 0.02482003746159184,
  "tail_sensor_speed_mean_m_s": -0.024761350411874748,
  "tail_fk_speed_mean_m_s": -0.024761682060327514,
  "peak_tilt_rad": 0.0777067700111349,
  "peak_wheel_torque_nm": 1.8540027141571045,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.03,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 24.149648716964293
}
```
