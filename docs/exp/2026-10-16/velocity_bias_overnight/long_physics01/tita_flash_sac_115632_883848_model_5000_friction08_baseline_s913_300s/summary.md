# tita_flash_sac_115632_883848_model_5000_friction08_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_friction08_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "c0fa3a831621244d92b2a89d915d88afff8850ae7288009dec0961a10ba6c445",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 35.496069068236444,
  "max_drift_m": 35.496069068236444,
  "radial_IAE_m_s": 6418.822897140748,
  "signed_longitudinal_delta_m": -0.9553771858614653,
  "tail_speed_mean_m_s": -0.16875684451076864,
  "tail_speed_rms_m_s": 0.16998146698420769,
  "tail_sensor_speed_mean_m_s": -0.16785742701689796,
  "tail_fk_speed_mean_m_s": -0.16790181148725064,
  "peak_tilt_rad": 0.07385492553619777,
  "peak_wheel_torque_nm": 3.884395122528076,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 64.86867943400284
}
```
