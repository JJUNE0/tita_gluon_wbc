# tita_flash_sac_115632_883848_model_65000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "1c603044b0fa168a181a326066cdb4e960662be66aaea143bdba25dbd311a0cc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008632597395972963,
  "max_drift_m": 0.008857025404306404,
  "radial_IAE_m_s": 0.4613793003741472,
  "signed_longitudinal_delta_m": 0.004277338553397321,
  "tail_speed_mean_m_s": 4.837906300107764e-05,
  "tail_speed_rms_m_s": 4.8379705126175025e-05,
  "tail_sensor_speed_mean_m_s": 2.7343818407591722e-05,
  "tail_fk_speed_mean_m_s": -1.510306242681728e-07,
  "peak_tilt_rad": 0.05325108901091369,
  "peak_wheel_torque_nm": 0.23751330375671387,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.026224852577034476,
  "final_integral_m_s": 0.026225141778767898,
  "elapsed_wall_s": 15.84454973397078
}
```
