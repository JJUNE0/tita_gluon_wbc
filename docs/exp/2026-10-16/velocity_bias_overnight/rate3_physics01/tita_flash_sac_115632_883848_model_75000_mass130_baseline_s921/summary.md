# tita_flash_sac_115632_883848_model_75000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "f2fc9a64dd3a4d1b28354ec9c5ec8f8828e570452ffe09fa6bf2ff128ba72bdc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.949196518269504,
  "max_drift_m": 12.949196518269504,
  "radial_IAE_m_s": 395.13557142230997,
  "signed_longitudinal_delta_m": -12.747008129719427,
  "tail_speed_mean_m_s": -0.20916852111508516,
  "tail_speed_rms_m_s": 0.20917658155665622,
  "tail_sensor_speed_mean_m_s": -0.20880458614321404,
  "tail_fk_speed_mean_m_s": -0.20880582893307786,
  "peak_tilt_rad": 0.023735771031549113,
  "peak_wheel_torque_nm": 0.27119553089141846,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.145971459976863
}
```
