# p000_tita_flash_sac_115632_883848_model_10000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p000_tita_flash_sac_115632_883848_model_10000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 0.0
    }
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "fbf923f95bdae04e5dc4d5798c4a53b03a4e9af4afaf8f4e506ae6e1ee828e9f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09446504493410601,
  "max_drift_m": 0.09727615863696885,
  "radial_IAE_m_s": 3.9997989633844657,
  "signed_longitudinal_delta_m": -0.09432816383007482,
  "tail_speed_mean_m_s": -0.0015250201856372855,
  "tail_speed_rms_m_s": 0.07029681935074049,
  "tail_sensor_speed_mean_m_s": -0.0036204354198616775,
  "tail_fk_speed_mean_m_s": -0.0006936097280212381,
  "peak_tilt_rad": 0.19872130456965476,
  "peak_wheel_torque_nm": 6.758861064910889,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5104893731009504,
  "final_integral_m_s": -0.5388495315216308,
  "elapsed_wall_s": 16.077977459004615
}
```
