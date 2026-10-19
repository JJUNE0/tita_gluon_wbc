# tita_flash_sac_193248_068255_model_80000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "e5ef314e33706dfccfa7e2bffc826ac1065299098cb20db40558a47d180c2cd4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.336362607265389,
  "max_drift_m": 6.336362607265389,
  "radial_IAE_m_s": 189.70344544234024,
  "signed_longitudinal_delta_m": -6.335616013294666,
  "tail_speed_mean_m_s": -0.10554935664213194,
  "tail_speed_rms_m_s": 0.10573099636500863,
  "tail_sensor_speed_mean_m_s": -0.10483925786271264,
  "tail_fk_speed_mean_m_s": -0.10528876576734872,
  "peak_tilt_rad": 0.06532676596524634,
  "peak_wheel_torque_nm": 3.41347599029541,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.244003515981603
}
```
