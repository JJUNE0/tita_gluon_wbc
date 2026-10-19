# tita_flash_sac_115632_883848_model_30000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "5e11d34b051317fa1d935ba245ff9a56f6665304d898c37adbe851a47c6b2b82",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.100575293182777,
  "max_drift_m": 13.100575293182777,
  "radial_IAE_m_s": 397.7221772237937,
  "signed_longitudinal_delta_m": 13.07977890249544,
  "tail_speed_mean_m_s": 0.21484745781420253,
  "tail_speed_rms_m_s": 0.21484758766707707,
  "tail_sensor_speed_mean_m_s": 0.21438215225474389,
  "tail_fk_speed_mean_m_s": 0.21438010107813776,
  "peak_tilt_rad": 0.1262132423279636,
  "peak_wheel_torque_nm": 0.14165425300598145,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.811146137013566
}
```
