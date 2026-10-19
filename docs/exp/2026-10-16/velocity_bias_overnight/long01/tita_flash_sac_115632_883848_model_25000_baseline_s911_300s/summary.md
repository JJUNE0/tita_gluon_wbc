# tita_flash_sac_115632_883848_model_25000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "d94b104327c8e147a9de69fb26214cd1864dcbbf974843d65e0950e8bc6829df",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 65.87724402224741,
  "max_drift_m": 66.38171057582373,
  "radial_IAE_m_s": 13198.07063131168,
  "signed_longitudinal_delta_m": -0.8658951264338467,
  "tail_speed_mean_m_s": 0.3736956431965867,
  "tail_speed_rms_m_s": 0.3737049693738976,
  "tail_sensor_speed_mean_m_s": 0.37291650878406113,
  "tail_fk_speed_mean_m_s": 0.3728981629364406,
  "peak_tilt_rad": 0.1403561925962551,
  "peak_wheel_torque_nm": 1.1433064937591553,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 48.940600342990365
}
```
