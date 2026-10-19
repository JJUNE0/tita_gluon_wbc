# tita_flash_sac_193248_068255_model_20000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
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
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "27746bc9fe5ae95431bb646c541dc3a18b63bd833d2b589f0f42124f6c084177",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.468073179518606,
  "max_drift_m": 4.468073179518606,
  "radial_IAE_m_s": 134.26957427558318,
  "signed_longitudinal_delta_m": 4.466611960376378,
  "tail_speed_mean_m_s": 0.07418661925459429,
  "tail_speed_rms_m_s": 0.07418664692640031,
  "tail_sensor_speed_mean_m_s": 0.07402776665777738,
  "tail_fk_speed_mean_m_s": 0.07402741881651483,
  "peak_tilt_rad": 0.14695689685020596,
  "peak_wheel_torque_nm": 0.37763166427612305,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.341870822012424
}
```
