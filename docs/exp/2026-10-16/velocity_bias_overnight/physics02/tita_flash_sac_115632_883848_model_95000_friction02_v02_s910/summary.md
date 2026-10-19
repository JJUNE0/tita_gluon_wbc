# tita_flash_sac_115632_883848_model_95000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "17e65aea4c83f5580e319d5c88e3e57140d4fb2d0d0b258ea2cff5a3d600026e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.040718422918598986,
  "max_drift_m": 0.05052624517095922,
  "radial_IAE_m_s": 2.755801690793112,
  "signed_longitudinal_delta_m": 0.04055486943469551,
  "tail_speed_mean_m_s": 9.21171994764016e-06,
  "tail_speed_rms_m_s": 9.236195784553179e-06,
  "tail_sensor_speed_mean_m_s": 5.075770001663925e-06,
  "tail_fk_speed_mean_m_s": 1.7682346200993528e-07,
  "peak_tilt_rad": 0.06444242064633898,
  "peak_wheel_torque_nm": 0.2756344676017761,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5124496015694531,
  "final_integral_m_s": 0.5124474793306493,
  "elapsed_wall_s": 14.631161383993458
}
```
