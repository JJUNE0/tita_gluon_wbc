# tita_flash_sac_115632_883848_model_10000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "5ad3d7ec80c73d3d8ec4b91a12750c3e8ca0884254e9d02cb25285acade770e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.4670540322264973,
  "max_drift_m": 1.4670540322264973,
  "radial_IAE_m_s": 47.09849156719453,
  "signed_longitudinal_delta_m": 1.4662844947184146,
  "tail_speed_mean_m_s": 0.02203232581996829,
  "tail_speed_rms_m_s": 0.024338202738829865,
  "tail_sensor_speed_mean_m_s": 0.023126041144954663,
  "tail_fk_speed_mean_m_s": 0.021748028252596495,
  "peak_tilt_rad": 0.12942986641691578,
  "peak_wheel_torque_nm": 5.543928146362305,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.370508445019368
}
```
