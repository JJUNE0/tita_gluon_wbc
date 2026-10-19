# tita_flash_sac_115632_883848_model_5000_com-0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com-0.005_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "31beae326f0d556d7c3e765e7fdfa18a5a4f0e97ffe23868f0c1b243a5c00dc4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08385508518746174,
  "max_drift_m": 0.09133951034366648,
  "radial_IAE_m_s": 5.045786550792088,
  "signed_longitudinal_delta_m": -0.08381256359070237,
  "tail_speed_mean_m_s": 1.3439963931269344e-05,
  "tail_speed_rms_m_s": 3.1806371748622676e-05,
  "tail_sensor_speed_mean_m_s": 1.740561714363831e-05,
  "tail_fk_speed_mean_m_s": 1.5445437346375815e-05,
  "peak_tilt_rad": 0.07771449119987994,
  "peak_wheel_torque_nm": 4.161378383636475,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.8722615630602409,
  "final_integral_m_s": -0.8722953160023075,
  "elapsed_wall_s": 5.4329194410238415
}
```
