# tita_flash_sac_115632_883848_model_5000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "initial_physics_sha256": "637283a5b2e9ddcead7b7916ba6b3b2a49dee1718c85341d1f9f634cd167da02",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.350855488272904,
  "max_drift_m": 9.350855488272904,
  "radial_IAE_m_s": 282.93701822135756,
  "signed_longitudinal_delta_m": -8.91536823367539,
  "tail_speed_mean_m_s": -0.15740971287019087,
  "tail_speed_rms_m_s": 0.1588501932588943,
  "tail_sensor_speed_mean_m_s": -0.15950815750414057,
  "tail_fk_speed_mean_m_s": -0.1568180082248915,
  "peak_tilt_rad": 0.06452076031233367,
  "peak_wheel_torque_nm": 3.7988388538360596,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.782248618954327
}
```
