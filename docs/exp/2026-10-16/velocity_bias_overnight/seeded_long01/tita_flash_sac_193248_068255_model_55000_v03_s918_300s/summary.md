# tita_flash_sac_193248_068255_model_55000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "7007bd893858d3d846314c2b2aeb7490d4df2049ec6d1e6bb5affb8b926a23fa",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.020423265817509643,
  "max_drift_m": 0.07825972189984055,
  "radial_IAE_m_s": 4.768282666288524,
  "signed_longitudinal_delta_m": 0.018134499803052536,
  "tail_speed_mean_m_s": 0.00016134272140517318,
  "tail_speed_rms_m_s": 0.00016313232984245489,
  "tail_sensor_speed_mean_m_s": 0.00015680068161386368,
  "tail_fk_speed_mean_m_s": 0.00015300705551193382,
  "peak_tilt_rad": 0.13777852572577576,
  "peak_wheel_torque_nm": 0.7942577600479126,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4773605462380204,
  "final_integral_m_s": 0.4773605462380204,
  "elapsed_wall_s": 43.33544819103554
}
```
