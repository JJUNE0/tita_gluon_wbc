# tita_flash_sac_115632_883848_model_65000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
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
  "initial_physics_sha256": "12ca94e455b99e23372ac0081f1f704358ba2a78ac3b5e267c82a2acd1ca4ddb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004795105826504531,
  "max_drift_m": 0.009985414676422043,
  "radial_IAE_m_s": 0.3078565322611698,
  "signed_longitudinal_delta_m": 0.004785579806571769,
  "tail_speed_mean_m_s": -9.296370987747748e-06,
  "tail_speed_rms_m_s": 9.309268540900803e-06,
  "tail_sensor_speed_mean_m_s": -9.060852437137316e-06,
  "tail_fk_speed_mean_m_s": -1.0244236134711875e-05,
  "peak_tilt_rad": 0.05701268681585647,
  "peak_wheel_torque_nm": 0.37404483556747437,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.049667755830727835,
  "final_integral_m_s": 0.04968691215991728,
  "elapsed_wall_s": 5.896066477987915
}
```
