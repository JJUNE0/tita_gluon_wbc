# tita_flash_sac_115632_883848_model_65000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "c2607dac168f2bbe35d201b5347e7f78d83271aca9242e2d49d84bc25807e196",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0013320208955966974,
  "max_drift_m": 0.011166462926635276,
  "radial_IAE_m_s": 0.0556604834511908,
  "signed_longitudinal_delta_m": -0.0013158496686034333,
  "tail_speed_mean_m_s": -2.532663054838501e-05,
  "tail_speed_rms_m_s": 2.535365937299618e-05,
  "tail_sensor_speed_mean_m_s": -2.5034506027884876e-05,
  "tail_fk_speed_mean_m_s": -2.6215573378629853e-05,
  "peak_tilt_rad": 0.056872617847645746,
  "peak_wheel_torque_nm": 0.3489862382411957,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.049989632043230585,
  "final_integral_m_s": 0.049989632043230585,
  "elapsed_wall_s": 5.633938087965362
}
```
