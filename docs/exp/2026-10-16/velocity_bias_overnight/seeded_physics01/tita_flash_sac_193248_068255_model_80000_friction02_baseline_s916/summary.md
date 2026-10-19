# tita_flash_sac_193248_068255_model_80000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "9f2cbfd6d34a65130f6b055b604a06acba43000f95c8f5388fdd56190c552965",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.567143084646493,
  "max_drift_m": 2.567143084646493,
  "radial_IAE_m_s": 70.64608817396136,
  "signed_longitudinal_delta_m": 2.542943222451963,
  "tail_speed_mean_m_s": 0.049228507494365685,
  "tail_speed_rms_m_s": 0.049323842754304334,
  "tail_sensor_speed_mean_m_s": 0.04983939824689829,
  "tail_fk_speed_mean_m_s": 0.04927323838534241,
  "peak_tilt_rad": 0.054270585989631304,
  "peak_wheel_torque_nm": 1.8052970170974731,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.047492455050815
}
```
