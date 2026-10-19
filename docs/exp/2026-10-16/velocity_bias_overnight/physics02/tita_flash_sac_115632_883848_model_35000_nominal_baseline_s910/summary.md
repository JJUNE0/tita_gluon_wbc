# tita_flash_sac_115632_883848_model_35000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
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
  "initial_physics_sha256": "fe14b691ca0e2c6f07d1edcfccd149a3a3a49bca81e0decc66b89a84b6f76983",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.798709971270828,
  "max_drift_m": 13.798709971270828,
  "radial_IAE_m_s": 410.68604343748177,
  "signed_longitudinal_delta_m": 13.79726783964267,
  "tail_speed_mean_m_s": 0.23248841342246973,
  "tail_speed_rms_m_s": 0.23248841607202964,
  "tail_sensor_speed_mean_m_s": 0.23198548295822952,
  "tail_fk_speed_mean_m_s": 0.2319835423262628,
  "peak_tilt_rad": 0.14046188265830772,
  "peak_wheel_torque_nm": 0.8796029090881348,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.477932033012621
}
```
