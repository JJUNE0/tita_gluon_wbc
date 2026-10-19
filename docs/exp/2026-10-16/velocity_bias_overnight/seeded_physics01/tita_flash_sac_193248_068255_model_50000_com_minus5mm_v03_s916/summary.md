# tita_flash_sac_193248_068255_model_50000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
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
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "645c896a00951229c495c17aefab1c57325abbbf2e709bd7a0c2577d8d0e2258",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.12576973578025258,
  "max_drift_m": 0.12576973578025258,
  "radial_IAE_m_s": 6.895554509510042,
  "signed_longitudinal_delta_m": 0.12576970418546743,
  "tail_speed_mean_m_s": 0.00013199461582341835,
  "tail_speed_rms_m_s": 0.00013399890977145663,
  "tail_sensor_speed_mean_m_s": 0.00013139134374906547,
  "tail_fk_speed_mean_m_s": 0.0001326801727623789,
  "peak_tilt_rad": 0.043735084694685566,
  "peak_wheel_torque_nm": 0.32797276973724365,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6440591188459293,
  "final_integral_m_s": 0.6440591188459293,
  "elapsed_wall_s": 10.25700921099633
}
```
