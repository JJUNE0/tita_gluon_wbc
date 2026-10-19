# tita_flash_sac_193248_068255_model_80000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
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
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "0f6fefdab08928bf1c77edc8271bba59b6e92064034a947e69c0e5958b26dacd",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 16.24653277285869,
  "max_drift_m": 16.24653277285869,
  "radial_IAE_m_s": 2273.466702138166,
  "signed_longitudinal_delta_m": 16.234102534348573,
  "tail_speed_mean_m_s": 0.060422333092001276,
  "tail_speed_rms_m_s": 0.06049275944382188,
  "tail_sensor_speed_mean_m_s": 0.05987042151877045,
  "tail_fk_speed_mean_m_s": 0.06043717638634568,
  "peak_tilt_rad": 0.05542290770063851,
  "peak_wheel_torque_nm": 2.2018160820007324,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 18.937443335016724
}
```
