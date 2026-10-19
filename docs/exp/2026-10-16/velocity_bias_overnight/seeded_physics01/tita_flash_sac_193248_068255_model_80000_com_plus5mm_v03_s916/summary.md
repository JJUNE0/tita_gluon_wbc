# tita_flash_sac_193248_068255_model_80000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "44c8b15ab5ca3fb1bbda0961f21da54fe70229161a64bb424df5063ba9f403be",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.054387596417566485,
  "max_drift_m": 0.05960107983373615,
  "radial_IAE_m_s": 3.159508126566908,
  "signed_longitudinal_delta_m": 0.05438349357478669,
  "tail_speed_mean_m_s": 3.086672494991972e-05,
  "tail_speed_rms_m_s": 3.114654410553566e-05,
  "tail_sensor_speed_mean_m_s": 3.061000352610203e-05,
  "tail_fk_speed_mean_m_s": 3.208693585267288e-05,
  "peak_tilt_rad": 0.05250749431963242,
  "peak_wheel_torque_nm": 1.9328235387802124,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2535665505477376,
  "final_integral_m_s": 0.2535665505477376,
  "elapsed_wall_s": 15.5778756380314
}
```
