# tita_flash_sac_115632_883848_model_60000_friction08_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction08_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "9064ed9941d862540cf642fcf2dbf29af5780286ee8c63e78bd4563550e065da",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.004220888183745853,
  "max_drift_m": 0.006998542023382662,
  "radial_IAE_m_s": 1.2914781109603797,
  "signed_longitudinal_delta_m": 0.004130169258988977,
  "tail_speed_mean_m_s": -3.0728698992712848e-06,
  "tail_speed_rms_m_s": 3.923989832837498e-06,
  "tail_sensor_speed_mean_m_s": -3.7126592208381212e-06,
  "tail_fk_speed_mean_m_s": -1.62277667352189e-06,
  "peak_tilt_rad": 0.0701125392875761,
  "peak_wheel_torque_nm": 0.2007516324520111,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.052637223466055386,
  "final_integral_m_s": 0.05263630080244456,
  "elapsed_wall_s": 44.306197794969194
}
```
