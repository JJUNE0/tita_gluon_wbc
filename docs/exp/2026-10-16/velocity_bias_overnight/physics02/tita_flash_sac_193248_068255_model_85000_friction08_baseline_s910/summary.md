# tita_flash_sac_193248_068255_model_85000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
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
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "9940532335cd91e772e26cd32bd8355dddefd65791e74313c0736dc8b7c7f473",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.810309877882092,
  "max_drift_m": 6.810309877882092,
  "radial_IAE_m_s": 197.7506829444489,
  "signed_longitudinal_delta_m": 6.809860781074119,
  "tail_speed_mean_m_s": 0.11929792686112742,
  "tail_speed_rms_m_s": 0.11929985698186202,
  "tail_sensor_speed_mean_m_s": 0.11904008147197806,
  "tail_fk_speed_mean_m_s": 0.11903810575773498,
  "peak_tilt_rad": 0.06866965096180522,
  "peak_wheel_torque_nm": 0.5040965676307678,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.321476257988252
}
```
