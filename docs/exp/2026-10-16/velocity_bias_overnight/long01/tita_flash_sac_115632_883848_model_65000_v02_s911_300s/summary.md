# tita_flash_sac_115632_883848_model_65000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "0d3896bada0cb7038442ae75fafacb146d8f88e18e776bd464859d825c426985",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.003818588483500595,
  "max_drift_m": 0.00998543496088416,
  "radial_IAE_m_s": 1.3102567355832062,
  "signed_longitudinal_delta_m": 0.0035446098045959873,
  "tail_speed_mean_m_s": -2.3070587793694465e-06,
  "tail_speed_rms_m_s": 2.3135309767822943e-06,
  "tail_sensor_speed_mean_m_s": -2.496537406494437e-06,
  "tail_fk_speed_mean_m_s": -4.127569026217297e-06,
  "peak_tilt_rad": 0.05701270594083985,
  "peak_wheel_torque_nm": 0.37404388189315796,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.03910568791954661,
  "final_integral_m_s": 0.03911339801159043,
  "elapsed_wall_s": 77.34945020900341
}
```
