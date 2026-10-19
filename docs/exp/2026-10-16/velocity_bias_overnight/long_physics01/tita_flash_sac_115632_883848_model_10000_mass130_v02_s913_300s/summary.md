# tita_flash_sac_115632_883848_model_10000_mass130_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass130_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "6cca400b41bf40e716da1cbefe646eb27c39f701a5ef2c77fc508d81f2b3998e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.19551713819892308,
  "max_drift_m": 0.19803436560446147,
  "radial_IAE_m_s": 35.673312696738094,
  "signed_longitudinal_delta_m": -0.19100454436547934,
  "tail_speed_mean_m_s": -0.00047846343972400476,
  "tail_speed_rms_m_s": 0.06251541611922795,
  "tail_sensor_speed_mean_m_s": 0.000234125948820946,
  "tail_fk_speed_mean_m_s": 1.2768637989078038e-05,
  "peak_tilt_rad": 0.19102658248581617,
  "peak_wheel_torque_nm": 6.373892307281494,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5723187347379579,
  "final_integral_m_s": -0.4637898810253289,
  "elapsed_wall_s": 69.41312149201985
}
```
