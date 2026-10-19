# tita_flash_sac_115632_883848_model_40000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "07b726c648ddbcd2d48722d025eef6733659e90439ef3606c5377cf34433902a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.1313059606880131,
  "max_drift_m": 1.1313059606880131,
  "radial_IAE_m_s": 33.675118326570356,
  "signed_longitudinal_delta_m": -1.1298208593655794,
  "tail_speed_mean_m_s": -0.019163954000589584,
  "tail_speed_rms_m_s": 0.019164164902498653,
  "tail_sensor_speed_mean_m_s": -0.01912286832904614,
  "tail_fk_speed_mean_m_s": -0.019122399441505872,
  "peak_tilt_rad": 0.09708607201996222,
  "peak_wheel_torque_nm": 0.2661059498786926,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.528736734995618
}
```
