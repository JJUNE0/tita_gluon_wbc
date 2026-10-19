# tita_flash_sac_115632_883848_model_80000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "initial_physics_sha256": "e66087af55f394adfc1cea35a61c1648b6f45160773693b27e280139f270d9ca",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08669778580812845,
  "max_drift_m": 0.0975690779095573,
  "radial_IAE_m_s": 5.508991300403981,
  "signed_longitudinal_delta_m": 0.08664259065299576,
  "tail_speed_mean_m_s": -7.049380900899282e-05,
  "tail_speed_rms_m_s": 7.049630569919011e-05,
  "tail_sensor_speed_mean_m_s": 0.00016139701946996514,
  "tail_fk_speed_mean_m_s": 4.3310922482334334e-08,
  "peak_tilt_rad": 0.08004356959470016,
  "peak_wheel_torque_nm": 0.42617204785346985,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8627774253386912,
  "final_integral_m_s": 0.8627790869157047,
  "elapsed_wall_s": 16.37669044896029
}
```
