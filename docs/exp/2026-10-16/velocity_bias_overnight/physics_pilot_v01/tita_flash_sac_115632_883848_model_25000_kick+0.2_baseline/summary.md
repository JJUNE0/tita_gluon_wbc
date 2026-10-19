# tita_flash_sac_115632_883848_model_25000_kick+0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick+0.2_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "7b256aa98a16b4b7feaae40c3db4b1513420c2633813a497dc374629ae5a215f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.0551612509893,
  "max_drift_m": 22.0551612509893,
  "radial_IAE_m_s": 669.3199500769397,
  "signed_longitudinal_delta_m": 20.99682197921347,
  "tail_speed_mean_m_s": 0.3736946641790406,
  "tail_speed_rms_m_s": 0.37370399114725467,
  "tail_sensor_speed_mean_m_s": 0.37290688118041987,
  "tail_fk_speed_mean_m_s": 0.3728976744154594,
  "peak_tilt_rad": 0.14253647529270785,
  "peak_wheel_torque_nm": 4.251437187194824,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.7811107079614885
}
```
