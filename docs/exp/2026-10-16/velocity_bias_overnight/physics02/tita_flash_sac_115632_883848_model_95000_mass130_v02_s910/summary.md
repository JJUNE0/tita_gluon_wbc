# tita_flash_sac_115632_883848_model_95000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "final_drift_m": 0.08029070838002188,
  "max_drift_m": 0.09769210222774849,
  "radial_IAE_m_s": 4.134366729724897,
  "signed_longitudinal_delta_m": -0.0802819700633686,
  "tail_speed_mean_m_s": -0.00040073198070441994,
  "tail_speed_rms_m_s": 0.015452869123885108,
  "tail_sensor_speed_mean_m_s": 1.7700937032716434e-05,
  "tail_fk_speed_mean_m_s": -7.973830957962878e-06,
  "peak_tilt_rad": 0.17012769331695954,
  "peak_wheel_torque_nm": 4.912603855133057,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.6019739983378236,
  "final_integral_m_s": -0.5913174935362876,
  "elapsed_wall_s": 18.482073300983757
}
```
