# tita_flash_sac_115632_883848_model_65000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "0b0ea84fb312f8f22c82c81b84b40bbf40755a5a19425fc53f0cca1ef3db600a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0027469901865887977,
  "max_drift_m": 0.08013283408299235,
  "radial_IAE_m_s": 0.2807419663258023,
  "signed_longitudinal_delta_m": -0.0026567947703845457,
  "tail_speed_mean_m_s": -2.4205459353441104e-05,
  "tail_speed_rms_m_s": 2.423256851065279e-05,
  "tail_sensor_speed_mean_m_s": -2.395258217498239e-05,
  "tail_fk_speed_mean_m_s": -2.514025837717781e-05,
  "peak_tilt_rad": 0.08264224141780607,
  "peak_wheel_torque_nm": 1.513182282447815,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.049456511596615814,
  "final_integral_m_s": 0.049456511596615814,
  "elapsed_wall_s": 9.11187773803249
}
```
