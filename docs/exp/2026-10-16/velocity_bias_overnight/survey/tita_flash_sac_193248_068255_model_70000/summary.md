# tita_flash_sac_193248_068255_model_70000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "12143eee71caa9583b9c58ed0da248a57aa8b919050f4e81451d19cdbd682fe5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.141553799444238,
  "max_drift_m": 3.141553799444238,
  "radial_IAE_m_s": 88.6410407449658,
  "signed_longitudinal_delta_m": 3.140132852226396,
  "tail_speed_mean_m_s": 0.05836110738782878,
  "tail_speed_rms_m_s": 0.05837702175196487,
  "tail_sensor_speed_mean_m_s": 0.05823538050457476,
  "tail_fk_speed_mean_m_s": 0.0582338458103494,
  "peak_tilt_rad": 0.08458977802481371,
  "peak_wheel_torque_nm": 0.02034744620323181,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.249913277046289
}
```
