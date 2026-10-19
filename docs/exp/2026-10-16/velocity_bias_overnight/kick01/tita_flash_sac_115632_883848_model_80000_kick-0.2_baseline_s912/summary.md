# tita_flash_sac_115632_883848_model_80000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "cfb5cd7764d3c98b50075737046bc85b54d0ad27c395b53026211398f9f76285",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.504247059552437,
  "max_drift_m": 11.504247059552437,
  "radial_IAE_m_s": 334.01761292426465,
  "signed_longitudinal_delta_m": 11.461350142393643,
  "tail_speed_mean_m_s": 0.19950705474137956,
  "tail_speed_rms_m_s": 0.19950736025809504,
  "tail_sensor_speed_mean_m_s": 0.19907611546965184,
  "tail_fk_speed_mean_m_s": 0.1990751310587179,
  "peak_tilt_rad": 0.08723047073338486,
  "peak_wheel_torque_nm": 1.9944065809249878,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.131109571026172
}
```
