# tita_flash_sac_115632_883848_model_10000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "ac71e583e26fbf2da3ad7475ed10fa6bf6cf734383d330cb67b04a6a11c39af3",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.06263181068285854,
  "max_drift_m": 0.06263181068285854,
  "radial_IAE_m_s": 13.37782141888563,
  "signed_longitudinal_delta_m": 0.06245796733389273,
  "tail_speed_mean_m_s": 0.00014625810826543936,
  "tail_speed_rms_m_s": 0.014279612327605041,
  "tail_sensor_speed_mean_m_s": 0.0010232004733275457,
  "tail_fk_speed_mean_m_s": 5.157460071051297e-05,
  "peak_tilt_rad": 0.11339596392135531,
  "peak_wheel_torque_nm": 2.943985939025879,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2814565364745468,
  "final_integral_m_s": 0.29500948262942633,
  "elapsed_wall_s": 83.64135456102667
}
```
