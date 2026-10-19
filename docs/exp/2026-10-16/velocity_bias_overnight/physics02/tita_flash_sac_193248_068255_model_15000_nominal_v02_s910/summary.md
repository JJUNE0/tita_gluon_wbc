# tita_flash_sac_193248_068255_model_15000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "d22b1bc83042cb3900a441c977ec5ff4574194f36a8fdc5255ff66dd20f27361",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017793340078172373,
  "max_drift_m": 0.024672093013599315,
  "radial_IAE_m_s": 1.0556457569341127,
  "signed_longitudinal_delta_m": -0.017791473341167187,
  "tail_speed_mean_m_s": -5.712051921773368e-06,
  "tail_speed_rms_m_s": 5.713284886094534e-06,
  "tail_sensor_speed_mean_m_s": -5.928877198547217e-06,
  "tail_fk_speed_mean_m_s": -3.6100841211250448e-06,
  "peak_tilt_rad": 0.09253866645050124,
  "peak_wheel_torque_nm": 0.4750027656555176,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18260167072057865,
  "final_integral_m_s": -0.1825944469161943,
  "elapsed_wall_s": 16.594996259955224
}
```
