# tita_flash_sac_115632_883848_model_5000_b+0.10

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_b+0.10",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": 0.1
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
  "initial_physics_sha256": "a14405f43198ecdfbefad595d127e0ed04bbd8d9cfddc7aaa119e9f369851b61",
  "complete": true,
  "failure": [],
  "duration_s": 40.0,
  "final_drift_m": 7.412147347607003,
  "max_drift_m": 7.412147347607003,
  "radial_IAE_m_s": 148.70830667603894,
  "signed_longitudinal_delta_m": -7.213173474476591,
  "tail_speed_mean_m_s": -0.18659534878603104,
  "tail_speed_rms_m_s": 0.18773402219401533,
  "tail_sensor_speed_mean_m_s": -0.18599679209284695,
  "tail_fk_speed_mean_m_s": -0.18577749739923516,
  "peak_tilt_rad": 0.08459715970551884,
  "peak_wheel_torque_nm": 3.9481656551361084,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.8085634890012443
}
```
