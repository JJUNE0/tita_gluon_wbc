# tita_flash_sac_193248_068255_model_70000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "e555bd403778e57140e6c9709f21aef54e610c08dcdf841b1fe09bcd95f8f064",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.3259897431270398,
  "max_drift_m": 3.3259897431270398,
  "radial_IAE_m_s": 100.2989606000917,
  "signed_longitudinal_delta_m": 3.3254181565202425,
  "tail_speed_mean_m_s": 0.057956037607966845,
  "tail_speed_rms_m_s": 0.057972709914897017,
  "tail_sensor_speed_mean_m_s": 0.057831205864921804,
  "tail_fk_speed_mean_m_s": 0.05782965898759665,
  "peak_tilt_rad": 0.09691597378950534,
  "peak_wheel_torque_nm": 1.5729241371154785,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.018119117012247
}
```
