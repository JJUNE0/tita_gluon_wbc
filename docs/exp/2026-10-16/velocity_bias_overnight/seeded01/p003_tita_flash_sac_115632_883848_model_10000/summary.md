# p003_tita_flash_sac_115632_883848_model_10000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p003_tita_flash_sac_115632_883848_model_10000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 0.5,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    }
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "final_drift_m": 0.12594780656897667,
  "max_drift_m": 0.12594780656897667,
  "radial_IAE_m_s": 4.95546046755482,
  "signed_longitudinal_delta_m": 0.12594552678553614,
  "tail_speed_mean_m_s": 0.0009035944909019451,
  "tail_speed_rms_m_s": 0.0009079969663165302,
  "tail_sensor_speed_mean_m_s": 0.0009015732942449007,
  "tail_fk_speed_mean_m_s": 0.0009013329697900187,
  "peak_tilt_rad": 0.11461661419631186,
  "peak_wheel_torque_nm": 2.0722358226776123,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.15452953141599945,
  "final_integral_m_s": -0.15452953141599945,
  "elapsed_wall_s": 5.382820605009329
}
```
