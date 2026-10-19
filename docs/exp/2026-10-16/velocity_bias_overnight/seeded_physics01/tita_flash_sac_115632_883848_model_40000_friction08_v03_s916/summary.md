# tita_flash_sac_115632_883848_model_40000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "b6de3e83e28f85379f3c42b2ceb359987e0c0bc5572a2b6bf9b48ea331d46235",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004625693332751458,
  "max_drift_m": 0.03920921645925211,
  "radial_IAE_m_s": 0.39770919436516405,
  "signed_longitudinal_delta_m": -0.004625653852649401,
  "tail_speed_mean_m_s": 4.6513455604140434e-05,
  "tail_speed_rms_m_s": 4.672881853061655e-05,
  "tail_sensor_speed_mean_m_s": 4.824063231398308e-05,
  "tail_fk_speed_mean_m_s": 5.0885677328288554e-05,
  "peak_tilt_rad": 0.11383307765199113,
  "peak_wheel_torque_nm": 0.8602372407913208,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.22939614707640363,
  "final_integral_m_s": 0.22939614707640363,
  "elapsed_wall_s": 12.628769983013626
}
```
