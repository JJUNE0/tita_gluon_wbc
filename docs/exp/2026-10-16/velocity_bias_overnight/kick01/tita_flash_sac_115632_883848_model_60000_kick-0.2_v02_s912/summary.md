# tita_flash_sac_115632_883848_model_60000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "1bc353e4989503690b72973268057bb806eb7d201bc6cadcf3253289a0c69ed8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0030309686334224943,
  "max_drift_m": 0.06088086736360768,
  "radial_IAE_m_s": 0.24781933881339713,
  "signed_longitudinal_delta_m": 0.0030020753859590736,
  "tail_speed_mean_m_s": -1.1350328477892454e-05,
  "tail_speed_rms_m_s": 1.1551469109802558e-05,
  "tail_sensor_speed_mean_m_s": -1.1409136644357703e-05,
  "tail_fk_speed_mean_m_s": -9.2826197319308e-06,
  "peak_tilt_rad": 0.11642958156864225,
  "peak_wheel_torque_nm": 1.6997427940368652,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.047607936865171216,
  "final_integral_m_s": 0.04762023765209332,
  "elapsed_wall_s": 16.27480860799551
}
```
