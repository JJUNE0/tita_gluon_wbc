# p004_tita_flash_sac_115632_883848_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p004_tita_flash_sac_115632_883848_model_25000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "gain_velocity": 0.05,
      "gain_floor": 0.1
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
  "initial_physics_sha256": "6a7623095d59b3790ae881c3fb20f5d23e46e39e8f7925b4c03378dac73ab1e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.24997935667840773,
  "max_drift_m": 0.24997935667840773,
  "radial_IAE_m_s": 11.999123669449856,
  "signed_longitudinal_delta_m": 0.24988595312489656,
  "tail_speed_mean_m_s": 0.0015786801096671038,
  "tail_speed_rms_m_s": 0.0015847066362430803,
  "tail_sensor_speed_mean_m_s": 0.001574854981117354,
  "tail_fk_speed_mean_m_s": 0.0015839096704088505,
  "peak_tilt_rad": 0.13977409659938833,
  "peak_wheel_torque_nm": 1.4628612995147705,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3379159494282227,
  "final_integral_m_s": 1.3376723873546492,
  "elapsed_wall_s": 11.068641841993667
}
```
