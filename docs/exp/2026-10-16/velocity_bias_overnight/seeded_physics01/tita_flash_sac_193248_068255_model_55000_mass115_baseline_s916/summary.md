# tita_flash_sac_193248_068255_model_55000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "f828a39bb923744fb73a32d472ffb0d83cab30f437b08343c61f5411631e54e8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.006101241735669,
  "max_drift_m": 9.006101241735669,
  "radial_IAE_m_s": 259.28697261560984,
  "signed_longitudinal_delta_m": 8.974805031352279,
  "tail_speed_mean_m_s": 0.15895593003819022,
  "tail_speed_rms_m_s": 0.15895614344544579,
  "tail_sensor_speed_mean_m_s": 0.15861346674471766,
  "tail_fk_speed_mean_m_s": 0.1586108262444396,
  "peak_tilt_rad": 0.1823709416072472,
  "peak_wheel_torque_nm": 0.21661412715911865,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.487314422964118
}
```
