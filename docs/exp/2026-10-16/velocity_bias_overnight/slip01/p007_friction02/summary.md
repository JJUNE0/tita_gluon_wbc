# p007_friction02

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p007_friction02",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "law": {
      "kp": -2.0,
      "ki": 5.0,
      "tau": 0.5,
      "ramp": 1.5,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 0.5
    },
    "estimator": "fk",
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "84a01faae86299146ddbc589eefbfe1c2819ae0d152720c81fbf0112950a2c58",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04774533953085218,
  "max_drift_m": 0.04797214969699157,
  "radial_IAE_m_s": 1.691613633184573,
  "signed_longitudinal_delta_m": -0.045713350141885066,
  "tail_speed_mean_m_s": -0.0006752283436295966,
  "tail_speed_rms_m_s": 0.00851190567553187,
  "tail_sensor_speed_mean_m_s": 6.434068651107922,
  "tail_fk_speed_mean_m_s": 6.43408703471988,
  "peak_tilt_rad": 0.6167434601173922,
  "peak_wheel_torque_nm": 5.954692840576172,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -2.0,
  "final_integral_m_s": 2.0,
  "elapsed_wall_s": 5.51829459995497
}
```
