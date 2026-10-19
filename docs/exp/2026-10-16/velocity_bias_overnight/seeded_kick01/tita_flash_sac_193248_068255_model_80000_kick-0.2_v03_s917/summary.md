# tita_flash_sac_193248_068255_model_80000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "3d031d68b0ed49e3f2a3c90802f8a8db44e3fdf004f9ff5638e1fe8c68376c7d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04940516293538666,
  "max_drift_m": 0.12626375502042503,
  "radial_IAE_m_s": 2.957672353986876,
  "signed_longitudinal_delta_m": 0.04940159808351981,
  "tail_speed_mean_m_s": 6.237622386558425e-05,
  "tail_speed_rms_m_s": 6.265780198008376e-05,
  "tail_sensor_speed_mean_m_s": 6.186107861472943e-05,
  "tail_fk_speed_mean_m_s": 6.332701923606955e-05,
  "peak_tilt_rad": 0.0626424914876238,
  "peak_wheel_torque_nm": 2.9264917373657227,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18058747358169916,
  "final_integral_m_s": 0.18058747358169916,
  "elapsed_wall_s": 12.21408079896355
}
```
