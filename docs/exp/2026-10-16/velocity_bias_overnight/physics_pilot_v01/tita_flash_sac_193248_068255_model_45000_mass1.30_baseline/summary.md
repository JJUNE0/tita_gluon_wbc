# tita_flash_sac_193248_068255_model_45000_mass1.30_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_mass1.30_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.3
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "87a864675134fdb77ed6ca3a2444317655c24ba4f47c7afaab40b982ec9747de",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.805160678089822,
  "max_drift_m": 12.805160678089822,
  "radial_IAE_m_s": 384.9302278034096,
  "signed_longitudinal_delta_m": -12.796691684626808,
  "tail_speed_mean_m_s": -0.21267716287242713,
  "tail_speed_rms_m_s": 0.21267771700462546,
  "tail_sensor_speed_mean_m_s": -0.2122024522855837,
  "tail_fk_speed_mean_m_s": -0.21222030597088842,
  "peak_tilt_rad": 0.02197305035142541,
  "peak_wheel_torque_nm": 0.3957592248916626,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.57914249796886
}
```
