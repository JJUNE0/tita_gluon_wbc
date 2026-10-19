# tita_flash_sac_115632_883848_model_30000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "17297fee2061fce9c518e57482c614c1ce3f6004be6932d9bf5dd3f13cf012ef",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.031967965676239586,
  "max_drift_m": 0.06361907976518717,
  "radial_IAE_m_s": 1.9205233014203296,
  "signed_longitudinal_delta_m": -0.03196759172140274,
  "tail_speed_mean_m_s": -3.9246272584121544e-06,
  "tail_speed_rms_m_s": 4.008120795907557e-06,
  "tail_sensor_speed_mean_m_s": -3.9158594663122e-06,
  "tail_fk_speed_mean_m_s": -3.823023343820033e-06,
  "peak_tilt_rad": 0.18609926174846314,
  "peak_wheel_torque_nm": 1.806382417678833,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3383333303346952,
  "final_integral_m_s": -0.33832838361096595,
  "elapsed_wall_s": 12.732555835973471
}
```
