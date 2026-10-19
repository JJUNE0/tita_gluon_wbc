# tita_flash_sac_115632_883848_model_75000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "d05a4a8eb1ba4aca662c6812282484bd1c59f6611a9003e62aefe54f6aa86c1d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0012004688919055075,
  "max_drift_m": 0.016103413844959544,
  "radial_IAE_m_s": 0.0712534580968267,
  "signed_longitudinal_delta_m": 0.0010919707634990115,
  "tail_speed_mean_m_s": 9.68082633105599e-06,
  "tail_speed_rms_m_s": 9.748893541052092e-06,
  "tail_sensor_speed_mean_m_s": 9.725716958120271e-06,
  "tail_fk_speed_mean_m_s": 1.037654373830317e-05,
  "peak_tilt_rad": 0.06197339509922206,
  "peak_wheel_torque_nm": 0.32116222381591797,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.004994676434898171,
  "final_integral_m_s": 0.0049718065978944,
  "elapsed_wall_s": 10.479246773000341
}
```
