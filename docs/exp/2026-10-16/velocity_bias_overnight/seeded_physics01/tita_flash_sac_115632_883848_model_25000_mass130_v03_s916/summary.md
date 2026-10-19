# tita_flash_sac_115632_883848_model_25000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "6ed7d243899e93f6b73a8dbce623dae284a932d9adc57d95dcb207753de9bb1a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0006222376916988651,
  "max_drift_m": 0.029165771173573007,
  "radial_IAE_m_s": 0.08360049530112507,
  "signed_longitudinal_delta_m": 0.0004543230024301271,
  "tail_speed_mean_m_s": 2.214803260461184e-06,
  "tail_speed_rms_m_s": 2.433733462555907e-06,
  "tail_sensor_speed_mean_m_s": 2.238916243582155e-06,
  "tail_fk_speed_mean_m_s": 2.8669818870725605e-06,
  "peak_tilt_rad": 0.11885664090034864,
  "peak_wheel_torque_nm": 1.277620792388916,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18138222289489966,
  "final_integral_m_s": 0.18138222289489966,
  "elapsed_wall_s": 12.083579158992507
}
```
