# tita_flash_sac_115632_883848_model_40000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "97958bd28f4ba36674627d6b97cd17be2dcfc06330fb89da1dd407fda52d68c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04425627685071858,
  "max_drift_m": 0.07384171722558834,
  "radial_IAE_m_s": 2.7160884262506246,
  "signed_longitudinal_delta_m": 0.04424768267981196,
  "tail_speed_mean_m_s": -3.8598239796879455e-05,
  "tail_speed_rms_m_s": 3.865222531266012e-05,
  "tail_sensor_speed_mean_m_s": -3.888314061070727e-05,
  "tail_fk_speed_mean_m_s": -4.007884604133804e-05,
  "peak_tilt_rad": 0.21346732650332578,
  "peak_wheel_torque_nm": 1.9544193744659424,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.27952338544791094,
  "final_integral_m_s": -0.27952338544791094,
  "elapsed_wall_s": 10.096744582988322
}
```
