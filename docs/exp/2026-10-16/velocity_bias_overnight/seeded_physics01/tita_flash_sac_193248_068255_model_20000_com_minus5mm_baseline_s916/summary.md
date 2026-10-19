# tita_flash_sac_193248_068255_model_20000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "48f09f9e360bd62c0fdd7de00d964fddc9f887eaa27a97bae5958cbfbdadbc88",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.191152173831906,
  "max_drift_m": 12.191152173831906,
  "radial_IAE_m_s": 365.7058978150001,
  "signed_longitudinal_delta_m": 12.169477384834817,
  "tail_speed_mean_m_s": 0.20446122833716002,
  "tail_speed_rms_m_s": 0.204461228594428,
  "tail_sensor_speed_mean_m_s": 0.2040199891216575,
  "tail_fk_speed_mean_m_s": 0.20400861774746679,
  "peak_tilt_rad": 0.153590970519353,
  "peak_wheel_torque_nm": 0.4553564786911011,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.797194441023748
}
```
