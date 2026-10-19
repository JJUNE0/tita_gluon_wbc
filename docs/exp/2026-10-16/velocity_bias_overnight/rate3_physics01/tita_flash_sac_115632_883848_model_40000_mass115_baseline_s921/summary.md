# tita_flash_sac_115632_883848_model_40000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "aa6f6007e6212c5157771efea7cef1a34da430fc84fb8d13a3bef35653a9c542",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.0912569999057045,
  "max_drift_m": 1.0912569999057045,
  "radial_IAE_m_s": 32.47110344547189,
  "signed_longitudinal_delta_m": -1.0898186753636407,
  "tail_speed_mean_m_s": -0.018496794613294013,
  "tail_speed_rms_m_s": 0.01849699754983818,
  "tail_sensor_speed_mean_m_s": -0.018457160086843578,
  "tail_fk_speed_mean_m_s": -0.01845667865910303,
  "peak_tilt_rad": 0.09753866356902496,
  "peak_wheel_torque_nm": 0.2679676115512848,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.055691480985843
}
```
