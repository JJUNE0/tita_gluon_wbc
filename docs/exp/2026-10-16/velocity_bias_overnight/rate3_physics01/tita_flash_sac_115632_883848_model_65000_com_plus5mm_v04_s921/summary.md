# tita_flash_sac_115632_883848_model_65000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "9414b5263419b86e5a154a9637b57bea4ff0a0eaffdefb6512a14ea8984b6e45",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010044408887116642,
  "max_drift_m": 0.02090009331711533,
  "radial_IAE_m_s": 0.5640227135812745,
  "signed_longitudinal_delta_m": -0.010039512544784633,
  "tail_speed_mean_m_s": -2.9951112236649457e-05,
  "tail_speed_rms_m_s": 3.015847630220995e-05,
  "tail_sensor_speed_mean_m_s": -2.9715606139719965e-05,
  "tail_fk_speed_mean_m_s": -3.1042286070547234e-05,
  "peak_tilt_rad": 0.060466104055423964,
  "peak_wheel_torque_nm": 0.5287330746650696,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08576861080994955,
  "final_integral_m_s": 0.08576861080994955,
  "elapsed_wall_s": 9.118943445035256
}
```
