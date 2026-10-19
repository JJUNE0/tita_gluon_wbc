# tita_flash_sac_193248_068255_model_80000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "f0ce01f418f1562536b0014cbb28de28624e896f5b85fe1e2ff1e3e549897797",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0008553769108888591,
  "max_drift_m": 0.03805315560604776,
  "radial_IAE_m_s": 0.4008283236430026,
  "signed_longitudinal_delta_m": -0.0008548241085951957,
  "tail_speed_mean_m_s": -0.00022634923068994294,
  "tail_speed_rms_m_s": 0.00674286315101588,
  "tail_sensor_speed_mean_m_s": 0.001181489203831242,
  "tail_fk_speed_mean_m_s": 0.0001858717181978551,
  "peak_tilt_rad": 0.09958779466625556,
  "peak_wheel_torque_nm": 3.958827018737793,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.21739616389362418,
  "final_integral_m_s": -0.21739616389362418,
  "elapsed_wall_s": 13.825062781979796
}
```
