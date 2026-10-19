# tita_flash_sac_193248_068255_model_70000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "7d106d78d3f67b7819e0b6e231f3f0551c3da8554afc2f7cd674d5f38c403962",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.6536335223124228,
  "max_drift_m": 2.6536335223124228,
  "radial_IAE_m_s": 71.59735737782181,
  "signed_longitudinal_delta_m": 2.6535857746580076,
  "tail_speed_mean_m_s": 0.05242591954006227,
  "tail_speed_rms_m_s": 0.05245975686349329,
  "tail_sensor_speed_mean_m_s": 0.05231308772148126,
  "tail_fk_speed_mean_m_s": 0.052311476535005445,
  "peak_tilt_rad": 0.08309650002693458,
  "peak_wheel_torque_nm": 0.04616657271981239,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.183966042008251
}
```
