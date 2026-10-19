# tita_flash_sac_115632_883848_model_80000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "ba50c423453b326fae223e3b41652322bbbfd8fd821c6b2fd07172d96ce7538e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08071041397693254,
  "max_drift_m": 0.0972931911265228,
  "radial_IAE_m_s": 4.713908444259509,
  "signed_longitudinal_delta_m": 0.08067696693843854,
  "tail_speed_mean_m_s": 5.159443959498983e-05,
  "tail_speed_rms_m_s": 5.412107921899142e-05,
  "tail_sensor_speed_mean_m_s": 5.1384401406319514e-05,
  "tail_fk_speed_mean_m_s": 5.1663361896997284e-05,
  "peak_tilt_rad": 0.08429464580853474,
  "peak_wheel_torque_nm": 0.6243147253990173,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8194880337769542,
  "final_integral_m_s": 0.8193788834929487,
  "elapsed_wall_s": 5.769975678005721
}
```
