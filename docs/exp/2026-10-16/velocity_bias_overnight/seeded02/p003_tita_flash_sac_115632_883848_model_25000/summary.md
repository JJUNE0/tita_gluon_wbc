# p003_tita_flash_sac_115632_883848_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p003_tita_flash_sac_115632_883848_model_25000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.5
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
  "final_drift_m": 0.053467356509979996,
  "max_drift_m": 0.20710355295396923,
  "radial_IAE_m_s": 2.7059082132623264,
  "signed_longitudinal_delta_m": 0.05344657977907364,
  "tail_speed_mean_m_s": 0.0003583951800385901,
  "tail_speed_rms_m_s": 0.0003642773775308035,
  "tail_sensor_speed_mean_m_s": 0.00035692619463080787,
  "tail_fk_speed_mean_m_s": 0.00036625615670799285,
  "peak_tilt_rad": 0.1659624754792428,
  "peak_wheel_torque_nm": 1.5633816719055176,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3431547623730105,
  "final_integral_m_s": 1.3431547623730105,
  "elapsed_wall_s": 4.7884543079999276
}
```
