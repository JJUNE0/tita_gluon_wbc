# p002_tita_flash_sac_115632_883848_model_10000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p002_tita_flash_sac_115632_883848_model_10000",
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
      "ki": 3.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.5
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
  "final_drift_m": 0.0348279564249946,
  "max_drift_m": 0.0348279564249946,
  "radial_IAE_m_s": 1.8019200205447952,
  "signed_longitudinal_delta_m": 0.0347801001097476,
  "tail_speed_mean_m_s": 0.00011763723237819713,
  "tail_speed_rms_m_s": 0.00011765884254869347,
  "tail_sensor_speed_mean_m_s": 0.000117427989834086,
  "tail_fk_speed_mean_m_s": 0.0001170431310313984,
  "peak_tilt_rad": 0.12891462511040408,
  "peak_wheel_torque_nm": 2.5181660652160645,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.15021415686329861,
  "final_integral_m_s": -0.15021415686329861,
  "elapsed_wall_s": 5.429763008956797
}
```
