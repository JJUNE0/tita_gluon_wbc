# tita_flash_sac_115632_883848_model_85000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "71ceeb909a0b22d4b4212b902e8cf78e5af20463e6379097f5346db5b559b5f0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09593383139107621,
  "max_drift_m": 0.16763484861211958,
  "radial_IAE_m_s": 5.8865996488173185,
  "signed_longitudinal_delta_m": 0.09593147874143361,
  "tail_speed_mean_m_s": -3.068464604380553e-06,
  "tail_speed_rms_m_s": 9.82163194744348e-06,
  "tail_sensor_speed_mean_m_s": -3.020400518918115e-06,
  "tail_fk_speed_mean_m_s": -2.714053708484473e-06,
  "peak_tilt_rad": 0.08116889662537874,
  "peak_wheel_torque_nm": 2.077798843383789,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.582613662458866,
  "final_integral_m_s": 0.582613662458866,
  "elapsed_wall_s": 8.411039297003299
}
```
