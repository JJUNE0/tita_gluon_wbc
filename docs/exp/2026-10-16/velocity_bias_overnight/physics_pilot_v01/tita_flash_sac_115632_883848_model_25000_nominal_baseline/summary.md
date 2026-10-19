# tita_flash_sac_115632_883848_model_25000_nominal_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_nominal_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.0,
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
  "initial_physics_sha256": "510e82e3500786a169fc86235fd90bfea6c849b554a650600290b4c1fe1749fe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.017526168505533,
  "max_drift_m": 22.017526168505533,
  "radial_IAE_m_s": 666.9802906196342,
  "signed_longitudinal_delta_m": 20.96321467793823,
  "tail_speed_mean_m_s": 0.3736939656058954,
  "tail_speed_rms_m_s": 0.37370329796699936,
  "tail_sensor_speed_mean_m_s": 0.37290748617628044,
  "tail_fk_speed_mean_m_s": 0.37289870947200704,
  "peak_tilt_rad": 0.13341076699959786,
  "peak_wheel_torque_nm": 0.6529412269592285,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.759016507014167
}
```
