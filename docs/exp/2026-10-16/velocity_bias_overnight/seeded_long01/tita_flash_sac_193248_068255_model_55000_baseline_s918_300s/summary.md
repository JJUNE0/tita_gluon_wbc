# tita_flash_sac_193248_068255_model_55000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 81.02863085149423,
  "max_drift_m": 81.02863085149423,
  "radial_IAE_m_s": 13174.24205279324,
  "signed_longitudinal_delta_m": 46.048902845706195,
  "tail_speed_mean_m_s": 0.3241111325428911,
  "tail_speed_rms_m_s": 0.3241111325464424,
  "tail_sensor_speed_mean_m_s": 0.3234102950394234,
  "tail_fk_speed_mean_m_s": 0.3234036077479101,
  "peak_tilt_rad": 0.17354901000802925,
  "peak_wheel_torque_nm": 0.2580503225326538,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 43.754215991008095
}
```
