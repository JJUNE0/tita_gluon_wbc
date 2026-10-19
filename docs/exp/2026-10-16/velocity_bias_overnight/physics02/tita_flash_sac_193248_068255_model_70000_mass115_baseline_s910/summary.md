# tita_flash_sac_193248_068255_model_70000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "281477c6672f58ef5bbfd0a2e6ad558d05a7bc8ac061569d1588645952bd8789",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.918108672764761,
  "max_drift_m": 5.918108672764761,
  "radial_IAE_m_s": 171.74972215749352,
  "signed_longitudinal_delta_m": -5.905806569519969,
  "tail_speed_mean_m_s": -0.10566025251623498,
  "tail_speed_rms_m_s": 0.10568708840697658,
  "tail_sensor_speed_mean_m_s": -0.10552532931571648,
  "tail_fk_speed_mean_m_s": -0.10552509492613074,
  "peak_tilt_rad": 0.07656170628718106,
  "peak_wheel_torque_nm": 0.3581646978855133,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.14597654598765
}
```
