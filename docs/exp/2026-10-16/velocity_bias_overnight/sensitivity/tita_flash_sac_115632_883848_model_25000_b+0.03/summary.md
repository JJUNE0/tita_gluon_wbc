# tita_flash_sac_115632_883848_model_25000_b+0.03

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_b+0.03",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": 0.03
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
  "initial_physics_sha256": "0a2be8f2ccd9994fba615ee2737982aba9ec6d63865dd5a06c4954e4fb5a7838",
  "complete": true,
  "failure": [],
  "duration_s": 40.0,
  "final_drift_m": 14.398052267347973,
  "max_drift_m": 14.398052267347973,
  "radial_IAE_m_s": 289.48679675120076,
  "signed_longitudinal_delta_m": 14.118961341240809,
  "tail_speed_mean_m_s": 0.3622324898186239,
  "tail_speed_rms_m_s": 0.3622410261815274,
  "tail_sensor_speed_mean_m_s": 0.36117148755705536,
  "tail_fk_speed_mean_m_s": 0.3614528504365037,
  "peak_tilt_rad": 0.1318759399405327,
  "peak_wheel_torque_nm": 0.6278506517410278,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.03,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.6174076659954153
}
```
