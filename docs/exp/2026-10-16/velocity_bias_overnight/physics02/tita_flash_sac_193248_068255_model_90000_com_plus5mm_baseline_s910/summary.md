# tita_flash_sac_193248_068255_model_90000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 15.872579490520007,
  "max_drift_m": 15.872579490520007,
  "radial_IAE_m_s": 466.7342151985031,
  "signed_longitudinal_delta_m": 15.868641665746544,
  "tail_speed_mean_m_s": 0.2720261701179782,
  "tail_speed_rms_m_s": 0.27202622707346696,
  "tail_sensor_speed_mean_m_s": 0.2714376145660415,
  "tail_fk_speed_mean_m_s": 0.2714354424074534,
  "peak_tilt_rad": 0.11794222000514032,
  "peak_wheel_torque_nm": 1.9773774147033691,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.614726832020096
}
```
