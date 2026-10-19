# tita_flash_sac_115632_883848_model_10000_mass130_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass130_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "6cca400b41bf40e716da1cbefe646eb27c39f701a5ef2c77fc508d81f2b3998e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 4.707350081321071,
  "max_drift_m": 4.719877771103618,
  "radial_IAE_m_s": 908.1616640430659,
  "signed_longitudinal_delta_m": -4.652247263855978,
  "tail_speed_mean_m_s": -0.008785714453040373,
  "tail_speed_rms_m_s": 0.008786285011621327,
  "tail_sensor_speed_mean_m_s": -0.008765788805975672,
  "tail_fk_speed_mean_m_s": -0.0087734521653068,
  "peak_tilt_rad": 0.08131833355301654,
  "peak_wheel_torque_nm": 1.853996753692627,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 53.677364050992765
}
```
