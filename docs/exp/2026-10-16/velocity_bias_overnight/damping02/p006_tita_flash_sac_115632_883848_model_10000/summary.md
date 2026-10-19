# p006_tita_flash_sac_115632_883848_model_10000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p006_tita_flash_sac_115632_883848_model_10000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 3.0
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
  "final_drift_m": 0.09398371472290916,
  "max_drift_m": 0.09448295858571057,
  "radial_IAE_m_s": 3.9244350766284057,
  "signed_longitudinal_delta_m": -0.0935093573551501,
  "tail_speed_mean_m_s": -0.0007232471481742913,
  "tail_speed_rms_m_s": 0.059270157046678186,
  "tail_sensor_speed_mean_m_s": -0.00023738054707188905,
  "tail_fk_speed_mean_m_s": 1.6359615534302108e-05,
  "peak_tilt_rad": 0.17872558358133483,
  "peak_wheel_torque_nm": 4.7080206871032715,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4504563748033787,
  "final_integral_m_s": -0.4762964531788259,
  "elapsed_wall_s": 13.53901416802546
}
```
