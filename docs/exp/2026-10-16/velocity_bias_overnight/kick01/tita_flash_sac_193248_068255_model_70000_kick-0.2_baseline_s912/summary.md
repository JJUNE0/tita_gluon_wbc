# tita_flash_sac_193248_068255_model_70000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "e8ed65e1f0293d7d0346b56c7a3cd24ad46228beb7a39ea30f65d8157757edb3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.6138003176949263,
  "max_drift_m": 2.6138003176949263,
  "radial_IAE_m_s": 64.76982489724143,
  "signed_longitudinal_delta_m": 2.6123929838000466,
  "tail_speed_mean_m_s": 0.05567587273970538,
  "tail_speed_rms_m_s": 0.055698666088665756,
  "tail_sensor_speed_mean_m_s": 0.0555560330894959,
  "tail_fk_speed_mean_m_s": 0.05555443552977262,
  "peak_tilt_rad": 0.08390229545295713,
  "peak_wheel_torque_nm": 1.6431154012680054,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.256336032995023
}
```
