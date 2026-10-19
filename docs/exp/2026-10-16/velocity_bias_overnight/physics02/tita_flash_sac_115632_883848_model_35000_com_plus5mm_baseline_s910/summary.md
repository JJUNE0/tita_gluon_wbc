# tita_flash_sac_115632_883848_model_35000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
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
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "79c32992af54fbb0b2828b612822fc0575bcd2d793e13f140ac72545a4a69c49",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.887241184111112,
  "max_drift_m": 14.887241184111112,
  "radial_IAE_m_s": 442.5304093405756,
  "signed_longitudinal_delta_m": 14.887199849967427,
  "tail_speed_mean_m_s": 0.2512904243544189,
  "tail_speed_rms_m_s": 0.2512904312391429,
  "tail_sensor_speed_mean_m_s": 0.250746799723671,
  "tail_fk_speed_mean_m_s": 0.250745129988079,
  "peak_tilt_rad": 0.14248129339680227,
  "peak_wheel_torque_nm": 0.7328535914421082,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.90275033301441
}
```
