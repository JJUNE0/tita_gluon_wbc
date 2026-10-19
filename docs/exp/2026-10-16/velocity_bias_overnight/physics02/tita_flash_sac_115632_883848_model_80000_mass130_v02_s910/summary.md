# tita_flash_sac_115632_883848_model_80000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "8e41887d3b3d5b66b07a549d648dfbad6d2b7656e708ce3d8d4243bb91844e6d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007181515868653808,
  "max_drift_m": 0.02004224247813054,
  "radial_IAE_m_s": 0.4113176032703265,
  "signed_longitudinal_delta_m": -0.007181033678693255,
  "tail_speed_mean_m_s": -2.322636066575617e-05,
  "tail_speed_rms_m_s": 2.3627059382249107e-05,
  "tail_sensor_speed_mean_m_s": -2.2532103732531795e-05,
  "tail_fk_speed_mean_m_s": -2.2610253903015646e-05,
  "peak_tilt_rad": 0.11337210500698647,
  "peak_wheel_torque_nm": 0.7598934173583984,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.07956364050923219,
  "final_integral_m_s": -0.07951517231505222,
  "elapsed_wall_s": 15.442163754021749
}
```
