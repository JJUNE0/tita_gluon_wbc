# tita_flash_sac_115632_883848_model_40000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "1597b62ccc93d4e793a7bff527630530b2354408e699dc55d9fb587cb6c68fa3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023645167322059336,
  "max_drift_m": 0.11346137422957875,
  "radial_IAE_m_s": 1.4745779121294258,
  "signed_longitudinal_delta_m": 0.023639980758048473,
  "tail_speed_mean_m_s": 1.7241707226181758e-05,
  "tail_speed_rms_m_s": 1.7317689644437962e-05,
  "tail_sensor_speed_mean_m_s": 1.6811391159820025e-05,
  "tail_fk_speed_mean_m_s": 1.9105640104197007e-05,
  "peak_tilt_rad": 0.14383498153658003,
  "peak_wheel_torque_nm": 2.203815221786499,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2383409510974759,
  "final_integral_m_s": 0.23829994896580817,
  "elapsed_wall_s": 12.05055112397531
}
```
