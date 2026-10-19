# tita_flash_sac_193248_068255_model_80000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "3d031d68b0ed49e3f2a3c90802f8a8db44e3fdf004f9ff5638e1fe8c68376c7d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.1621547636012504,
  "max_drift_m": 2.1621547636012504,
  "radial_IAE_m_s": 52.936236385645486,
  "signed_longitudinal_delta_m": 2.1603658628692455,
  "tail_speed_mean_m_s": 0.0466973281535818,
  "tail_speed_rms_m_s": 0.04679825339168596,
  "tail_sensor_speed_mean_m_s": 0.04604675714913053,
  "tail_fk_speed_mean_m_s": 0.046739151993924755,
  "peak_tilt_rad": 0.05406124773556398,
  "peak_wheel_torque_nm": 2.8955655097961426,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.244781194021925
}
```
