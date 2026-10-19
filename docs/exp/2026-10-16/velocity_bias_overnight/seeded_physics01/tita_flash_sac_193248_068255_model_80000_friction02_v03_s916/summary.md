# tita_flash_sac_193248_068255_model_80000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "9f2cbfd6d34a65130f6b055b604a06acba43000f95c8f5388fdd56190c552965",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04698874428407487,
  "max_drift_m": 0.04698874428407487,
  "radial_IAE_m_s": 2.5993599754679106,
  "signed_longitudinal_delta_m": 0.04698490656349214,
  "tail_speed_mean_m_s": 6.949112024223489e-05,
  "tail_speed_rms_m_s": 6.987224722370163e-05,
  "tail_sensor_speed_mean_m_s": 7.315884540003152e-05,
  "tail_fk_speed_mean_m_s": 7.517435656703147e-05,
  "peak_tilt_rad": 0.05045505986690846,
  "peak_wheel_torque_nm": 1.7843555212020874,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18164912446404316,
  "final_integral_m_s": 0.18164912446404316,
  "elapsed_wall_s": 14.572548652009573
}
```
