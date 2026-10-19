# tita_flash_sac_115632_883848_model_75000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "final_drift_m": 0.029862475498983854,
  "max_drift_m": 0.059917331008883086,
  "radial_IAE_m_s": 1.8226869000193204,
  "signed_longitudinal_delta_m": -0.02986247346824286,
  "tail_speed_mean_m_s": 1.3460050320180887e-05,
  "tail_speed_rms_m_s": 1.3525619430355821e-05,
  "tail_sensor_speed_mean_m_s": 1.34558963683875e-05,
  "tail_fk_speed_mean_m_s": 1.39582821646819e-05,
  "peak_tilt_rad": 0.11629758129426682,
  "peak_wheel_torque_nm": 0.8172881603240967,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.31568273206013125,
  "final_integral_m_s": -0.3157150761194873,
  "elapsed_wall_s": 13.231710507010575
}
```
