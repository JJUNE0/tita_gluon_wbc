# tita_flash_sac_193248_068255_model_70000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "97e7a9f3b2767c48a9b011e2677e0fb6777168cf72ad493a2e22b36d3a734273",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015848962285750827,
  "max_drift_m": 0.1199297711512029,
  "radial_IAE_m_s": 1.0284065952421217,
  "signed_longitudinal_delta_m": 0.015848169299587427,
  "tail_speed_mean_m_s": 6.538005482743749e-05,
  "tail_speed_rms_m_s": 6.57634312958434e-05,
  "tail_sensor_speed_mean_m_s": 6.537204243180233e-05,
  "tail_fk_speed_mean_m_s": 6.510860408722698e-05,
  "peak_tilt_rad": 0.09636322945034959,
  "peak_wheel_torque_nm": 1.5983059406280518,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0857512175165203,
  "final_integral_m_s": 0.0857512175165203,
  "elapsed_wall_s": 11.355545143946074
}
```
