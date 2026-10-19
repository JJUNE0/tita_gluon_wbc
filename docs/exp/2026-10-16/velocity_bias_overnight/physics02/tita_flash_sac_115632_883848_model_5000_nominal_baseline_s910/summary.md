# tita_flash_sac_115632_883848_model_5000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "2f491c6051ffa90074a4c339f034d92dbbbe51740597259ac78cca40f029c33d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.044108805984493,
  "max_drift_m": 10.044108805984493,
  "radial_IAE_m_s": 304.2151996501896,
  "signed_longitudinal_delta_m": -9.52602197424832,
  "tail_speed_mean_m_s": -0.16909886047891867,
  "tail_speed_rms_m_s": 0.17032891194108377,
  "tail_sensor_speed_mean_m_s": -0.16839412934444584,
  "tail_fk_speed_mean_m_s": -0.1682510940567294,
  "peak_tilt_rad": 0.07369309669963409,
  "peak_wheel_torque_nm": 3.8925678730010986,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.857812787988223
}
```
