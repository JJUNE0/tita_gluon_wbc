# tita_flash_sac_115632_883848_model_25000_baseline_s914_900s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_baseline_s914_900s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 900.0,
    "warmup": 1.2,
    "seed": 914,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "4b812bd34d609053b1d507c064f920b9ae4e59441ee42ae070bdf43bd8cae15a",
  "complete": true,
  "failure": [],
  "duration_s": 900.0,
  "final_drift_m": 61.864756480315975,
  "max_drift_m": 66.37803346628813,
  "radial_IAE_m_s": 39514.14525742207,
  "signed_longitudinal_delta_m": -15.998325328640272,
  "tail_speed_mean_m_s": 0.3736942953148606,
  "tail_speed_rms_m_s": 0.3737036241529715,
  "tail_sensor_speed_mean_m_s": 0.37290444897402125,
  "tail_fk_speed_mean_m_s": 0.37289775294521776,
  "peak_tilt_rad": 0.14041111452643995,
  "peak_wheel_torque_nm": 1.150740385055542,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 135.97239802096738
}
```
