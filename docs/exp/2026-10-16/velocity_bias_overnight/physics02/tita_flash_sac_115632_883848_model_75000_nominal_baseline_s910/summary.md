# tita_flash_sac_115632_883848_model_75000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "d05a4a8eb1ba4aca662c6812282484bd1c59f6611a9003e62aefe54f6aa86c1d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01337703996481609,
  "max_drift_m": 0.049771234164668485,
  "radial_IAE_m_s": 2.355544220284321,
  "signed_longitudinal_delta_m": -0.013285503749309218,
  "tail_speed_mean_m_s": 0.001215207040185122,
  "tail_speed_rms_m_s": 0.0012331142579353033,
  "tail_sensor_speed_mean_m_s": 0.0012126794148942085,
  "tail_fk_speed_mean_m_s": 0.0012131780346061858,
  "peak_tilt_rad": 0.051944132586105196,
  "peak_wheel_torque_nm": 0.15532687306404114,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.35483408201253
}
```
