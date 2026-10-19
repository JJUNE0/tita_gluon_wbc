# p007_tita_flash_sac_115632_883848_model_10000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p007_tita_flash_sac_115632_883848_model_10000",
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
      "ki": 15.0,
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
  "final_drift_m": 0.06195998230272771,
  "max_drift_m": 0.0786543597885966,
  "radial_IAE_m_s": 2.981158460575611,
  "signed_longitudinal_delta_m": -0.06190609575820564,
  "tail_speed_mean_m_s": 8.037083939852698e-05,
  "tail_speed_rms_m_s": 0.05844952174289396,
  "tail_sensor_speed_mean_m_s": 0.0034035214366058713,
  "tail_fk_speed_mean_m_s": 0.0008162720632010596,
  "peak_tilt_rad": 0.17735633319882393,
  "peak_wheel_torque_nm": 4.465638637542725,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3653297603938068,
  "final_integral_m_s": -0.45451864735066755,
  "elapsed_wall_s": 16.200387306977063
}
```
