# tita_flash_sac_193248_068255_model_5000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "4bb46314f84c1b73e05a68fef6eb2c1b8d60bc9aaa199dd53e6d7c43abeaf9d8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.20334460047223557,
  "max_drift_m": 0.2061645753241538,
  "radial_IAE_m_s": 11.648607618705771,
  "signed_longitudinal_delta_m": -0.20327222673267784,
  "tail_speed_mean_m_s": 5.617406654854959e-05,
  "tail_speed_rms_m_s": 5.787200037600996e-05,
  "tail_sensor_speed_mean_m_s": 4.651039780452993e-05,
  "tail_fk_speed_mean_m_s": 3.9041862167580474e-05,
  "peak_tilt_rad": 0.07477299469123744,
  "peak_wheel_torque_nm": 1.1568379402160645,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0164699256339693,
  "final_integral_m_s": -1.0164699256339693,
  "elapsed_wall_s": 13.81299309298629
}
```
