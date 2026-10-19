# tita_flash_sac_193248_068255_model_15000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "final_drift_m": 0.01938685425526981,
  "max_drift_m": 0.05769663396156144,
  "radial_IAE_m_s": 1.1658074658718653,
  "signed_longitudinal_delta_m": -0.019386366270981756,
  "tail_speed_mean_m_s": -5.752971413138367e-06,
  "tail_speed_rms_m_s": 5.753664657850773e-06,
  "tail_sensor_speed_mean_m_s": -5.978831072372881e-06,
  "tail_fk_speed_mean_m_s": -3.6481245728605855e-06,
  "peak_tilt_rad": 0.15188386372831353,
  "peak_wheel_torque_nm": 3.6273725032806396,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.183216132940749,
  "final_integral_m_s": -0.18320869823839778,
  "elapsed_wall_s": 14.643022914009634
}
```
