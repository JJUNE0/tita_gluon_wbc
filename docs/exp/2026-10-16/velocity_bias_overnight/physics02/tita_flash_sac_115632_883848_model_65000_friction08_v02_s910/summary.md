# tita_flash_sac_115632_883848_model_65000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "e7d19762292e6b20fdb6e92dee1c7e9e45ad12e0285b240ca4e37346c6e77d6f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005090303696664385,
  "max_drift_m": 0.009973686266055694,
  "radial_IAE_m_s": 0.32279876565451887,
  "signed_longitudinal_delta_m": 0.005076817035349264,
  "tail_speed_mean_m_s": -1.0898735802177977e-05,
  "tail_speed_rms_m_s": 1.0911840386809e-05,
  "tail_sensor_speed_mean_m_s": -1.0533978280483252e-05,
  "tail_fk_speed_mean_m_s": -1.1690268453206427e-05,
  "peak_tilt_rad": 0.05689364088974935,
  "peak_wheel_torque_nm": 0.35665953159332275,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.05161287634365609,
  "final_integral_m_s": 0.0516347911439564,
  "elapsed_wall_s": 15.220510184008162
}
```
