# tita_flash_sac_115632_883848_model_5000_com_plus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_plus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "f05b2a32cd66439a7c3ed981ab578ef10dec11d2f3cd0ca490cf37d00c0d5878",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 34.61588565411511,
  "max_drift_m": 34.61588565411511,
  "radial_IAE_m_s": 6103.091964117694,
  "signed_longitudinal_delta_m": -7.270684566348446,
  "tail_speed_mean_m_s": -0.15666313427090045,
  "tail_speed_rms_m_s": 0.1580910075470026,
  "tail_sensor_speed_mean_m_s": -0.15337030612200783,
  "tail_fk_speed_mean_m_s": -0.15608121778106446,
  "peak_tilt_rad": 0.06434702220430699,
  "peak_wheel_torque_nm": 3.7989869117736816,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 71.85056934296153
}
```
