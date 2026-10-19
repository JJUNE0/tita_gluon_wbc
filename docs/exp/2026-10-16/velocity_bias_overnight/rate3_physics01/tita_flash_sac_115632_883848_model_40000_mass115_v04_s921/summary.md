# tita_flash_sac_115632_883848_model_40000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "aa6f6007e6212c5157771efea7cef1a34da430fc84fb8d13a3bef35653a9c542",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004549094689301001,
  "max_drift_m": 0.010056443327131865,
  "radial_IAE_m_s": 0.30721539355027816,
  "signed_longitudinal_delta_m": 0.0045462752133515055,
  "tail_speed_mean_m_s": -2.063173340501919e-05,
  "tail_speed_rms_m_s": 2.1364743912475092e-05,
  "tail_sensor_speed_mean_m_s": -2.0529039205396558e-05,
  "tail_fk_speed_mean_m_s": -2.0102855425526985e-05,
  "peak_tilt_rad": 0.11285112225008453,
  "peak_wheel_torque_nm": 0.38937583565711975,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03699875947187599,
  "final_integral_m_s": -0.03699875947187599,
  "elapsed_wall_s": 9.848293392977212
}
```
