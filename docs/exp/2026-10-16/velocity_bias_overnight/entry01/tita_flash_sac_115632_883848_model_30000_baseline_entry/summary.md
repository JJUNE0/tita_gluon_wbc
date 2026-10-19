# tita_flash_sac_115632_883848_model_30000_baseline_entry

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: FAIL

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "FAIL",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_baseline_entry",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 0.0,
    "seed": 272,
    "estimator": "fk",
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
  "initial_physics_sha256": "72d010b3d1fa79251553f54fdf3c0d7dde3b25d889f42f3a2ef092efbbc33587",
  "complete": false,
  "failure": [
    "base_height_limit",
    "leg_joint_limit"
  ],
  "duration_s": 0.0,
  "final_drift_m": 0.0,
  "max_drift_m": 0.0,
  "radial_IAE_m_s": 0.0,
  "signed_longitudinal_delta_m": 0.0,
  "tail_speed_mean_m_s": null,
  "tail_speed_rms_m_s": null,
  "tail_sensor_speed_mean_m_s": null,
  "tail_fk_speed_mean_m_s": null,
  "peak_tilt_rad": 0.11992663034275308,
  "peak_wheel_torque_nm": 0.0,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 0.12311927601695061
}
```
