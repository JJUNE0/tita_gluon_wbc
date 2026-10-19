# tita_flash_sac_193248_068255_model_80000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "648af24e3af170804bb1ea69a206d23e73f6cc0e68c9730c69cebf29b9630fa9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06228047058314544,
  "max_drift_m": 0.06499827016675916,
  "radial_IAE_m_s": 2.627932505179724,
  "signed_longitudinal_delta_m": -0.06227001336834376,
  "tail_speed_mean_m_s": -0.0005332940500335798,
  "tail_speed_rms_m_s": 0.02083723921967964,
  "tail_sensor_speed_mean_m_s": 0.0033927430757614333,
  "tail_fk_speed_mean_m_s": 0.00013079652011067577,
  "peak_tilt_rad": 0.17193772746670843,
  "peak_wheel_torque_nm": 6.106008052825928,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.232553058346978,
  "final_integral_m_s": -0.25255200560411656,
  "elapsed_wall_s": 14.786540811008308
}
```
