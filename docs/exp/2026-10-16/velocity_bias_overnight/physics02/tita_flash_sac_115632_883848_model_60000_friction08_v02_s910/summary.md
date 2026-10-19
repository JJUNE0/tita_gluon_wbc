# tita_flash_sac_115632_883848_model_60000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
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
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "4cfcca0685b5cec90e026911fe8500beee893ba5594f5a671cfc80b7ccdb33b6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004388334414209306,
  "max_drift_m": 0.00699061975403971,
  "radial_IAE_m_s": 0.2640600440051842,
  "signed_longitudinal_delta_m": 0.00438185781543394,
  "tail_speed_mean_m_s": -8.3128772875669e-07,
  "tail_speed_rms_m_s": 9.366008781595408e-06,
  "tail_sensor_speed_mean_m_s": -7.410515344695932e-07,
  "tail_fk_speed_mean_m_s": 1.3800206124850824e-06,
  "peak_tilt_rad": 0.07005947371364751,
  "peak_wheel_torque_nm": 0.20008012652397156,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0488295237445141,
  "final_integral_m_s": 0.04885016976794444,
  "elapsed_wall_s": 14.788591274991632
}
```
