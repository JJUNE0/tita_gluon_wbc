# tita_flash_sac_115632_883848_model_25000_friction08_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction08_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "37e50b7c69a29e6e553fe648da32835dc13dbd5813cf07b679fd72f34dbae7fc",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 70.606715526238,
  "max_drift_m": 70.62400979461755,
  "radial_IAE_m_s": 13591.727567278416,
  "signed_longitudinal_delta_m": 8.033429926190589,
  "tail_speed_mean_m_s": 0.37358561218389214,
  "tail_speed_rms_m_s": 0.3735947716959397,
  "tail_sensor_speed_mean_m_s": 0.3728159997190429,
  "tail_fk_speed_mean_m_s": 0.37279884815620523,
  "peak_tilt_rad": 0.13925212808112342,
  "peak_wheel_torque_nm": 1.103438377380371,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 45.03645728598349
}
```
