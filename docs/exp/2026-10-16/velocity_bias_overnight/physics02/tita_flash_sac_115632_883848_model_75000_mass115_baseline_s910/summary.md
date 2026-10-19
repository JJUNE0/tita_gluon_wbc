# tita_flash_sac_115632_883848_model_75000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
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
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "d3a07c7bf36d1c6af0f06a362c0f1a5eb79cb8434057884572eac89bf544fa21",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.51803853748976,
  "max_drift_m": 7.51803853748976,
  "radial_IAE_m_s": 229.13736132522095,
  "signed_longitudinal_delta_m": -7.475143340554801,
  "tail_speed_mean_m_s": -0.12189794204804462,
  "tail_speed_rms_m_s": 0.12190248209257504,
  "tail_sensor_speed_mean_m_s": -0.12163423805366169,
  "tail_fk_speed_mean_m_s": -0.12163172780623793,
  "peak_tilt_rad": 0.020605662154197013,
  "peak_wheel_torque_nm": 0.12074536085128784,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.812378761009313
}
```
