# tita_flash_sac_193248_068255_model_90000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "03c64566712d7de94d8a16d6045773f2979249082c0dfa3db30027440f1ef36c",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.1102146888104573,
  "max_drift_m": 0.1102146888104573,
  "radial_IAE_m_s": 29.79982382535649,
  "signed_longitudinal_delta_m": 0.11018301631544342,
  "tail_speed_mean_m_s": 1.9576292280126544e-05,
  "tail_speed_rms_m_s": 2.6009329411286895e-05,
  "tail_sensor_speed_mean_m_s": 2.427229926187206e-05,
  "tail_fk_speed_mean_m_s": 2.922997955517032e-05,
  "peak_tilt_rad": 0.10162929361109474,
  "peak_wheel_torque_nm": 1.677504301071167,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.7150365949979327,
  "final_integral_m_s": 0.7150365949979327,
  "elapsed_wall_s": 19.061808687984012
}
```
