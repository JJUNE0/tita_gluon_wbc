# tita_flash_sac_115632_883848_model_25000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "eb5f3687019017a742c82823f57c28b9568eedb2ec54b69c358dd1adcc57147e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07589894276467758,
  "max_drift_m": 0.12966219098011963,
  "radial_IAE_m_s": 3.8719131842281245,
  "signed_longitudinal_delta_m": 0.07589860892611212,
  "tail_speed_mean_m_s": 0.00040033448341037485,
  "tail_speed_rms_m_s": 0.0004020182317095233,
  "tail_sensor_speed_mean_m_s": 0.00040003731790785527,
  "tail_fk_speed_mean_m_s": 0.0004094902567957491,
  "peak_tilt_rad": 0.13084807079648741,
  "peak_wheel_torque_nm": 1.29961097240448,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3366416363794327,
  "final_integral_m_s": 1.3366416363794327,
  "elapsed_wall_s": 8.653585510968696
}
```
