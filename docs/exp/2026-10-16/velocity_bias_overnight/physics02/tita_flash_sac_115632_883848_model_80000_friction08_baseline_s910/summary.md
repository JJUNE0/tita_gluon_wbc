# tita_flash_sac_115632_883848_model_80000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "a3281e6647dd4018ca6b6b58f5587de1f4f7be4ed36aa3205324c7606510453a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.650509155908763,
  "max_drift_m": 11.650509155908763,
  "radial_IAE_m_s": 343.2425850522782,
  "signed_longitudinal_delta_m": 11.526577600734814,
  "tail_speed_mean_m_s": 0.19945529453945549,
  "tail_speed_rms_m_s": 0.19945563075935388,
  "tail_sensor_speed_mean_m_s": 0.19902446442685495,
  "tail_fk_speed_mean_m_s": 0.19902348152611726,
  "peak_tilt_rad": 0.08678629647474234,
  "peak_wheel_torque_nm": 0.4092063307762146,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.508322321984451
}
```
