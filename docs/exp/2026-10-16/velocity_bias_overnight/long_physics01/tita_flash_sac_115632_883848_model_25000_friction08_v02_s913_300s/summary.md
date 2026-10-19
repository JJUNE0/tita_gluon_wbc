# tita_flash_sac_115632_883848_model_25000_friction08_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction08_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "final_drift_m": 0.1461299902486849,
  "max_drift_m": 0.21262134677380154,
  "radial_IAE_m_s": 45.30967082526608,
  "signed_longitudinal_delta_m": 0.14573203548829725,
  "tail_speed_mean_m_s": -9.665578304171066e-05,
  "tail_speed_rms_m_s": 9.675355462113796e-05,
  "tail_sensor_speed_mean_m_s": -0.00010299377928360189,
  "tail_fk_speed_mean_m_s": -8.469055346835444e-05,
  "peak_tilt_rad": 0.13859376912461485,
  "peak_wheel_torque_nm": 1.432308316230774,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.2705558196743159,
  "final_integral_m_s": 1.2707411852964612,
  "elapsed_wall_s": 58.95393250900088
}
```
