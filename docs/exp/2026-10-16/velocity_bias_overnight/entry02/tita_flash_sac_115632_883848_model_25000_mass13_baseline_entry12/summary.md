# tita_flash_sac_115632_883848_model_25000_mass13_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass13_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "9fbc79c4932327d686aca26d9a9ffc7af09003dc2cbf88d8b0bbbc1c7ae32dcb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.512371827700963,
  "max_drift_m": 5.512371827700963,
  "radial_IAE_m_s": 165.21315144394308,
  "signed_longitudinal_delta_m": 5.503271476701335,
  "tail_speed_mean_m_s": 0.09193540964162661,
  "tail_speed_rms_m_s": 0.09193542510069855,
  "tail_sensor_speed_mean_m_s": 0.09173792929493778,
  "tail_fk_speed_mean_m_s": 0.09173585945955112,
  "peak_tilt_rad": 0.1197305619014648,
  "peak_wheel_torque_nm": 1.2776191234588623,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.872317785979249
}
```
