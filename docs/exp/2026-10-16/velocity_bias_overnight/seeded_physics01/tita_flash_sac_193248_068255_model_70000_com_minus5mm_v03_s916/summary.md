# tita_flash_sac_193248_068255_model_70000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "7bfc116c39ba3ca64e6e59d94792aba5cbedf7d7b2ae281c03494d91a7145c35",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020201654204855663,
  "max_drift_m": 0.026346914748951324,
  "radial_IAE_m_s": 1.058725759096227,
  "signed_longitudinal_delta_m": 0.02020156134086191,
  "tail_speed_mean_m_s": 7.949592206976525e-05,
  "tail_speed_rms_m_s": 7.95651678534416e-05,
  "tail_sensor_speed_mean_m_s": 7.945885359569305e-05,
  "tail_fk_speed_mean_m_s": 7.921404590373813e-05,
  "peak_tilt_rad": 0.07922828391483083,
  "peak_wheel_torque_nm": 0.22829517722129822,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.00832888540583383,
  "final_integral_m_s": 0.00832888540583383,
  "elapsed_wall_s": 11.86485522100702
}
```
