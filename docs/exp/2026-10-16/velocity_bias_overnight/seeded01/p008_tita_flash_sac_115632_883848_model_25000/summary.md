# p008_tita_flash_sac_115632_883848_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p008_tita_flash_sac_115632_883848_model_25000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 2.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 4.0
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
  "initial_physics_sha256": "6a7623095d59b3790ae881c3fb20f5d23e46e39e8f7925b4c03378dac73ab1e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03153093560127866,
  "max_drift_m": 0.2080170738716755,
  "radial_IAE_m_s": 1.2682861501213718,
  "signed_longitudinal_delta_m": 0.031530039071311335,
  "tail_speed_mean_m_s": 0.000760649837835572,
  "tail_speed_rms_m_s": 0.0007682002842417695,
  "tail_sensor_speed_mean_m_s": 0.0007585668496260684,
  "tail_fk_speed_mean_m_s": 0.0007678477326277411,
  "peak_tilt_rad": 0.1393772974641705,
  "peak_wheel_torque_nm": 1.5686193704605103,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3404025887786684,
  "final_integral_m_s": 1.3404025887786684,
  "elapsed_wall_s": 4.558454437996261
}
```
