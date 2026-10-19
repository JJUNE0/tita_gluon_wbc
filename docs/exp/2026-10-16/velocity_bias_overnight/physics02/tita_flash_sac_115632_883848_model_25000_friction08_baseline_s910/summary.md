# tita_flash_sac_115632_883848_model_25000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "ff49cf8cc939df45c1bbf9dda89ab64bd18c889da93a10e6e80d6e0117aaa725",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.099526439323167,
  "max_drift_m": 22.099526439323167,
  "radial_IAE_m_s": 668.0055946164716,
  "signed_longitudinal_delta_m": 21.67808686203295,
  "tail_speed_mean_m_s": 0.37358398063781156,
  "tail_speed_rms_m_s": 0.37359314771875407,
  "tail_sensor_speed_mean_m_s": 0.3728064866910787,
  "tail_fk_speed_mean_m_s": 0.37279996244258456,
  "peak_tilt_rad": 0.13933588447898004,
  "peak_wheel_torque_nm": 1.1040550470352173,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.718705866020173
}
```
