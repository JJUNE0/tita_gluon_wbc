# tita_flash_sac_115632_883848_model_5000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "7c0faf89760deeecf0199a742f4dc9111c0f284b116c5d0d9d6006df57efd7d8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.80862243996608,
  "max_drift_m": 10.80862243996608,
  "radial_IAE_m_s": 327.67581734260716,
  "signed_longitudinal_delta_m": -10.182067344919686,
  "tail_speed_mean_m_s": -0.1820482562736822,
  "tail_speed_rms_m_s": 0.1830321280875435,
  "tail_sensor_speed_mean_m_s": -0.1795171601196423,
  "tail_fk_speed_mean_m_s": -0.18135532292197726,
  "peak_tilt_rad": 0.08247972427908423,
  "peak_wheel_torque_nm": 3.888861656188965,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.393303891993128
}
```
