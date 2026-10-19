# tita_flash_sac_115632_883848_model_10000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "f8094877dc459d696cabffa8432c131655bdea2884bdd250e365bc0ba3393bbe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.030940372878060736,
  "max_drift_m": 0.035734831242171645,
  "radial_IAE_m_s": 1.696523400880786,
  "signed_longitudinal_delta_m": -0.03083527908040207,
  "tail_speed_mean_m_s": 3.538085113575273e-05,
  "tail_speed_rms_m_s": 0.03673591546882299,
  "tail_sensor_speed_mean_m_s": 0.0025556185269287393,
  "tail_fk_speed_mean_m_s": 0.0003042657251904047,
  "peak_tilt_rad": 0.14406688586073169,
  "peak_wheel_torque_nm": 5.066474437713623,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.20206810634762884,
  "final_integral_m_s": -0.25705708481513573,
  "elapsed_wall_s": 17.60768775298493
}
```
