# tita_flash_sac_193248_068255_model_70000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "8f8550e1dffbb870d2048ef4b7dc79bca6357d911381bf0ab163e48c52c56bbe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03337931942272848,
  "max_drift_m": 0.10855400003400201,
  "radial_IAE_m_s": 4.2437993114659385,
  "signed_longitudinal_delta_m": 0.03337383475916663,
  "tail_speed_mean_m_s": 0.0058295454343660754,
  "tail_speed_rms_m_s": 0.005945954512605605,
  "tail_sensor_speed_mean_m_s": 0.005817556583281965,
  "tail_fk_speed_mean_m_s": 0.005816466932172971,
  "peak_tilt_rad": 0.07325253718908509,
  "peak_wheel_torque_nm": 0.03426934778690338,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.336294188979082
}
```
