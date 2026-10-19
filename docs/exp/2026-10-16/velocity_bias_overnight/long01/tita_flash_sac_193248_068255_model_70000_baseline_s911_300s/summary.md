# tita_flash_sac_193248_068255_model_70000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "5c17d70585c31a487c359a247c6892174a6c845ec95c8b33c520266fc65773cd",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 18.48701977552902,
  "max_drift_m": 18.48701977552902,
  "radial_IAE_m_s": 2643.5998406747212,
  "signed_longitudinal_delta_m": 18.14941745060184,
  "tail_speed_mean_m_s": 0.06622763784161066,
  "tail_speed_rms_m_s": 0.06622763821417298,
  "tail_sensor_speed_mean_m_s": 0.06608421873239387,
  "tail_fk_speed_mean_m_s": 0.06608318521032265,
  "peak_tilt_rad": 0.08706490026195612,
  "peak_wheel_torque_nm": 0.057361140847206116,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 59.90129321598215
}
```
