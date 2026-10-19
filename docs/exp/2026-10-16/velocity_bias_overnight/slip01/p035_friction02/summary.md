# p035_friction02

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p035_friction02",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
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
  "final_drift_m": 0.14392525578950796,
  "max_drift_m": 0.1440567995226201,
  "radial_IAE_m_s": 4.112525953880248,
  "signed_longitudinal_delta_m": -0.14392112193046908,
  "tail_speed_mean_m_s": -0.0023552209993112434,
  "tail_speed_rms_m_s": 0.009640541157765066,
  "tail_sensor_speed_mean_m_s": 9.717150117934853,
  "tail_fk_speed_mean_m_s": 9.717075279865824,
  "peak_tilt_rad": 0.6485809660309374,
  "peak_wheel_torque_nm": 5.710300445556641,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 2.0,
  "final_integral_m_s": 0.18548259246221344,
  "elapsed_wall_s": 5.6308963560150005
}
```
