# tita_flash_sac_115632_883848_model_95000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "f6d17812d4193ea97c35c4826ff2365355bed55badcd7410ed2635309515be17",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.337476600673313,
  "max_drift_m": 11.337476600673313,
  "radial_IAE_m_s": 342.5511359614672,
  "signed_longitudinal_delta_m": -11.337095599902124,
  "tail_speed_mean_m_s": -0.1857848233848745,
  "tail_speed_rms_m_s": 0.18578935906178698,
  "tail_sensor_speed_mean_m_s": -0.18538524614268995,
  "tail_fk_speed_mean_m_s": -0.18538572165358463,
  "peak_tilt_rad": 0.03871755790800946,
  "peak_wheel_torque_nm": 0.5306281447410583,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.94817874598084
}
```
