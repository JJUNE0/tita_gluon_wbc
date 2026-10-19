# tita_flash_sac_193248_068255_model_15000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "c2f3ab32bc7e736d5eaa674b7bccd72d478aa722e950befba59d9e4b4bccce2b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01808417774302447,
  "max_drift_m": 0.024210440040611157,
  "radial_IAE_m_s": 1.056489559605624,
  "signed_longitudinal_delta_m": -0.018081730794941218,
  "tail_speed_mean_m_s": -1.1792646803077979e-05,
  "tail_speed_rms_m_s": 1.1861080047316213e-05,
  "tail_sensor_speed_mean_m_s": -7.309283134987797e-06,
  "tail_fk_speed_mean_m_s": -4.316541726823751e-06,
  "peak_tilt_rad": 0.09115225291953433,
  "peak_wheel_torque_nm": 0.46241798996925354,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1817217042218466,
  "final_integral_m_s": -0.18171366797667307,
  "elapsed_wall_s": 20.354933932016138
}
```
