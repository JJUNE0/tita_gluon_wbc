# tita_flash_sac_115632_883848_model_75000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "f80fdbca30805398d95cd6d8cd76ba8033f957528da011b46721f51fa5cf7faf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.019497503829664403,
  "max_drift_m": 0.04920907598419929,
  "radial_IAE_m_s": 2.4679438856004383,
  "signed_longitudinal_delta_m": -0.01944691696404917,
  "tail_speed_mean_m_s": 0.00106597704022604,
  "tail_speed_rms_m_s": 0.001080742117667618,
  "tail_sensor_speed_mean_m_s": 0.0010637806802442085,
  "tail_fk_speed_mean_m_s": 0.0010642785259955842,
  "peak_tilt_rad": 0.051903047394999735,
  "peak_wheel_torque_nm": 0.15775296092033386,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.238999271008652
}
```
