# tita_flash_sac_115632_883848_model_25000_mass115_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass115_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "85ad07916ff3bbea9b742e19b248b5892347d5bfd6af9460aa4611511f1915cf",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 59.77923241299629,
  "max_drift_m": 59.77923241299629,
  "radial_IAE_m_s": 10176.97005321556,
  "signed_longitudinal_delta_m": 26.02851500504013,
  "tail_speed_mean_m_s": 0.2546714877714051,
  "tail_speed_rms_m_s": 0.25468035618127083,
  "tail_sensor_speed_mean_m_s": 0.2541922177402076,
  "tail_fk_speed_mean_m_s": 0.2541142252898796,
  "peak_tilt_rad": 0.13311013579585773,
  "peak_wheel_torque_nm": 1.262876033782959,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 45.520702715963125
}
```
