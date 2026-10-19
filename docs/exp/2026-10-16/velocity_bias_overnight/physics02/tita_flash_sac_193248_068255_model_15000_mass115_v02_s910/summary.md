# tita_flash_sac_193248_068255_model_15000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "e14c90838f319d7dd3057ff2ddccccb5704f8fec9a457442d5b515a6a7abadf9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03154113812168942,
  "max_drift_m": 0.033860309903710965,
  "radial_IAE_m_s": 1.8947165272995383,
  "signed_longitudinal_delta_m": -0.031541106067006865,
  "tail_speed_mean_m_s": 9.062304142762723e-06,
  "tail_speed_rms_m_s": 9.096221424736738e-06,
  "tail_sensor_speed_mean_m_s": 9.73625329223729e-06,
  "tail_fk_speed_mean_m_s": 1.2587733060399384e-05,
  "peak_tilt_rad": 0.13560422917327686,
  "peak_wheel_torque_nm": 2.7090563774108887,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3366894392230646,
  "final_integral_m_s": -0.33671242990732775,
  "elapsed_wall_s": 18.326010306016542
}
```
