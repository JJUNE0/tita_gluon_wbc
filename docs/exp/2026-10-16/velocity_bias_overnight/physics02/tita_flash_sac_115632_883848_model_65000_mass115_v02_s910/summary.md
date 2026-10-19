# tita_flash_sac_115632_883848_model_65000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "c12475c4b45d12c261f882656e3dcb5d894a98d01453d8dbea41c46bcfec0d98",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.019906164851625986,
  "max_drift_m": 0.04765548592879015,
  "radial_IAE_m_s": 1.2039086982843583,
  "signed_longitudinal_delta_m": -0.019899718701361667,
  "tail_speed_mean_m_s": -4.6678391601321744e-07,
  "tail_speed_rms_m_s": 6.125171380669464e-07,
  "tail_sensor_speed_mean_m_s": -6.103310703306855e-07,
  "tail_fk_speed_mean_m_s": -1.865196913536255e-06,
  "peak_tilt_rad": 0.11018593217229711,
  "peak_wheel_torque_nm": 0.9981970191001892,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.21419049810641916,
  "final_integral_m_s": -0.21418799168564678,
  "elapsed_wall_s": 17.540656512021087
}
```
