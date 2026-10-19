# tita_flash_sac_193248_068255_model_15000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "cc2f4bfacf14b116ec3d681a94782a0da7d5168f7d7527ba2aa134b8166ef917",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.4867242365749127,
  "max_drift_m": 3.4867242365749127,
  "radial_IAE_m_s": 106.49283697926974,
  "signed_longitudinal_delta_m": -3.486621606531197,
  "tail_speed_mean_m_s": -0.05690120743561631,
  "tail_speed_rms_m_s": 0.05690127760689387,
  "tail_sensor_speed_mean_m_s": -0.056812042587744055,
  "tail_fk_speed_mean_m_s": -0.05681195219068581,
  "peak_tilt_rad": 0.08955120949395146,
  "peak_wheel_torque_nm": 3.7924020290374756,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.719539135985542
}
```
