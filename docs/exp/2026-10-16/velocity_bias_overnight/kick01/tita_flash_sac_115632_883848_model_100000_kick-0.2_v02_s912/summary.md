# tita_flash_sac_115632_883848_model_100000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "bfe5755e59d9190ba4d27d4878a2fbf0ac973dc4fc7c0eed032d81b60cee9f7c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05209641612235458,
  "max_drift_m": 0.06729988349875674,
  "radial_IAE_m_s": 3.020029249141617,
  "signed_longitudinal_delta_m": 0.052094391229555365,
  "tail_speed_mean_m_s": 3.833304238101892e-05,
  "tail_speed_rms_m_s": 3.854723960790767e-05,
  "tail_sensor_speed_mean_m_s": 3.8079825331465035e-05,
  "tail_fk_speed_mean_m_s": 3.8082120631135397e-05,
  "peak_tilt_rad": 0.09768362162212796,
  "peak_wheel_torque_nm": 2.160259246826172,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.542875033987627,
  "final_integral_m_s": 0.5427984060069275,
  "elapsed_wall_s": 15.123431371001061
}
```
