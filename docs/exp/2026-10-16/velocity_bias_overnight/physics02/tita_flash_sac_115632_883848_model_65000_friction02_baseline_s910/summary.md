# tita_flash_sac_115632_883848_model_65000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "1c603044b0fa168a181a326066cdb4e960662be66aaea143bdba25dbd311a0cc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.1575179550109769,
  "max_drift_m": 1.1575179550109769,
  "radial_IAE_m_s": 37.29167390323282,
  "signed_longitudinal_delta_m": 0.7831518814908365,
  "tail_speed_mean_m_s": 0.021015172616802018,
  "tail_speed_rms_m_s": 0.02102104396215131,
  "tail_sensor_speed_mean_m_s": 0.02065072142756667,
  "tail_fk_speed_mean_m_s": 0.020625887545723844,
  "peak_tilt_rad": 0.05475040205124282,
  "peak_wheel_torque_nm": 0.1719144582748413,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.250714479014277
}
```
