# tita_flash_sac_193248_068255_model_90000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "556f42300d229dba9db974d5ad64a16bf8b6486a539a6c2da39a644df78bec6f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06844281767508006,
  "max_drift_m": 0.08845338831136228,
  "radial_IAE_m_s": 3.9863735679901158,
  "signed_longitudinal_delta_m": 0.06843905297480997,
  "tail_speed_mean_m_s": 4.69557687615789e-05,
  "tail_speed_rms_m_s": 4.8199532398140795e-05,
  "tail_sensor_speed_mean_m_s": 4.710365941574371e-05,
  "tail_fk_speed_mean_m_s": 4.846280332083561e-05,
  "peak_tilt_rad": 0.10608262675144675,
  "peak_wheel_torque_nm": 1.5299692153930664,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.691100920086121,
  "final_integral_m_s": 0.6910255876404284,
  "elapsed_wall_s": 17.447976498981006
}
```
