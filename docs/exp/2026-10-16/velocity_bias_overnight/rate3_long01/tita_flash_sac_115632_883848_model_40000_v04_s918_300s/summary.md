# tita_flash_sac_115632_883848_model_40000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "7aec6b1b690a57bd4b5bde62c7bf29b0a80c7dade549dd36853e4d25b9e5493f",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.004602162445576939,
  "max_drift_m": 0.039765688572142896,
  "radial_IAE_m_s": 1.2980877332791922,
  "signed_longitudinal_delta_m": -0.004529678861492615,
  "tail_speed_mean_m_s": -9.39345942915822e-06,
  "tail_speed_rms_m_s": 9.400504052282036e-06,
  "tail_sensor_speed_mean_m_s": -9.267036054878414e-06,
  "tail_fk_speed_mean_m_s": -7.529809958746271e-06,
  "peak_tilt_rad": 0.11353210889158705,
  "peak_wheel_torque_nm": 0.8933029770851135,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2370550430530724,
  "final_integral_m_s": 0.2370550430530724,
  "elapsed_wall_s": 55.88363182998728
}
```
