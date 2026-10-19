# tita_flash_sac_193248_068255_model_20000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "32eb33d395ab1db4a49313db0c4b033371796ef1312e6544bd345e25d00b93ad",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 58.33234830983763,
  "max_drift_m": 58.33234830983763,
  "radial_IAE_m_s": 9284.817391256149,
  "signed_longitudinal_delta_m": 43.65564613670792,
  "tail_speed_mean_m_s": 0.2184889946000735,
  "tail_speed_rms_m_s": 0.21848899460089877,
  "tail_sensor_speed_mean_m_s": 0.21801742461714618,
  "tail_fk_speed_mean_m_s": 0.2180075842815105,
  "peak_tilt_rad": 0.1595664352476378,
  "peak_wheel_torque_nm": 0.40743446350097656,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 43.070298156002536
}
```
