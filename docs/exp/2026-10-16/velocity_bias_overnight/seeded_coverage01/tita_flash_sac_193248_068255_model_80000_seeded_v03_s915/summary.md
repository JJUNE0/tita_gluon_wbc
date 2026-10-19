# tita_flash_sac_193248_068255_model_80000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
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
  "initial_physics_sha256": "af873898e1269e68ec40759a7f5942bf3f441702f1d94c02f44465db2c82e6a2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06488064714364745,
  "max_drift_m": 0.06488064714364745,
  "radial_IAE_m_s": 3.6739344657260684,
  "signed_longitudinal_delta_m": 0.06487963372959064,
  "tail_speed_mean_m_s": 5.455364923259361e-05,
  "tail_speed_rms_m_s": 5.455933002755291e-05,
  "tail_sensor_speed_mean_m_s": 5.4146721221322776e-05,
  "tail_fk_speed_mean_m_s": 5.5551737238023204e-05,
  "peak_tilt_rad": 0.052565513160415245,
  "peak_wheel_torque_nm": 2.2198479175567627,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18509210888013297,
  "final_integral_m_s": 0.18509210888013297,
  "elapsed_wall_s": 4.644228814984672
}
```
