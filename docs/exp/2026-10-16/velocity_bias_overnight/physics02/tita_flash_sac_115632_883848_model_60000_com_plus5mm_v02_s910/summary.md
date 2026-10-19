# tita_flash_sac_115632_883848_model_60000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "f052f5232b3cb1b42cd05f4045153eef9a497d6e8b47dfc45ef6ff9aeeb47746",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008696838688322363,
  "max_drift_m": 0.015244341981631073,
  "radial_IAE_m_s": 0.5518373632626778,
  "signed_longitudinal_delta_m": 0.008695200159838922,
  "tail_speed_mean_m_s": -1.6196503202539653e-05,
  "tail_speed_rms_m_s": 1.6212681424075674e-05,
  "tail_sensor_speed_mean_m_s": -1.6294071946108485e-05,
  "tail_fk_speed_mean_m_s": -1.4336212747020402e-05,
  "peak_tilt_rad": 0.07336839318326382,
  "peak_wheel_torque_nm": 0.3012726306915283,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.09195112140991418,
  "final_integral_m_s": 0.09197789246964869,
  "elapsed_wall_s": 18.747046045958996
}
```
