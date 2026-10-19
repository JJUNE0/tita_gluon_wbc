# tita_flash_sac_193248_068255_model_85000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "ae995617f5ac22560d3e6f23738b63cf213512da0f03b1ba859111ac68d02fb5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.932153234171191,
  "max_drift_m": 6.932153234171191,
  "radial_IAE_m_s": 202.8351956040911,
  "signed_longitudinal_delta_m": 6.928350510256721,
  "tail_speed_mean_m_s": 0.12006400147850181,
  "tail_speed_rms_m_s": 0.1200653830951793,
  "tail_sensor_speed_mean_m_s": 0.11980453361816513,
  "tail_fk_speed_mean_m_s": 0.11980249356037175,
  "peak_tilt_rad": 0.06884059844624368,
  "peak_wheel_torque_nm": 0.5152266025543213,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.794202478951775
}
```
