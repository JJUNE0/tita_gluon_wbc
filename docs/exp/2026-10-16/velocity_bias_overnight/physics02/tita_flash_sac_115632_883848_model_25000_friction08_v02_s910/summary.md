# tita_flash_sac_115632_883848_model_25000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
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
  "initial_physics_sha256": "ff49cf8cc939df45c1bbf9dda89ab64bd18c889da93a10e6e80d6e0117aaa725",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.15239391811968467,
  "max_drift_m": 0.21269050146193055,
  "radial_IAE_m_s": 8.839375109142228,
  "signed_longitudinal_delta_m": 0.15238992998454387,
  "tail_speed_mean_m_s": 0.0001681468259430184,
  "tail_speed_rms_m_s": 0.00016835011394612337,
  "tail_sensor_speed_mean_m_s": 0.00017689806456520744,
  "tail_fk_speed_mean_m_s": 0.00018863251431148882,
  "peak_tilt_rad": 0.13868070707842683,
  "peak_wheel_torque_nm": 1.4305751323699951,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.334098245315777,
  "final_integral_m_s": 1.3337833860836197,
  "elapsed_wall_s": 12.373665385006461
}
```
