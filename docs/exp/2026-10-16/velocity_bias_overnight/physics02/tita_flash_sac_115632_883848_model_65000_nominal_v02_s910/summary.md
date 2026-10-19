# tita_flash_sac_115632_883848_model_65000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "a63eaf010b0c141571cf8f6267bae4a8ef07e2c30535073bc45fa22cc0eb46a2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004776591329885949,
  "max_drift_m": 0.009976114349826651,
  "radial_IAE_m_s": 0.3065608565643264,
  "signed_longitudinal_delta_m": 0.004766907925510242,
  "tail_speed_mean_m_s": -9.123459171991071e-06,
  "tail_speed_rms_m_s": 9.136257063553167e-06,
  "tail_sensor_speed_mean_m_s": -8.900602399577615e-06,
  "tail_fk_speed_mean_m_s": -1.008745848378089e-05,
  "peak_tilt_rad": 0.056988764712511575,
  "peak_wheel_torque_nm": 0.3740306496620178,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04947369414025041,
  "final_integral_m_s": 0.04949230433569189,
  "elapsed_wall_s": 14.529908169992268
}
```
