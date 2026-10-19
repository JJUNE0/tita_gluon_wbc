# tita_flash_sac_193248_068255_model_5000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "c22ab1310630f8725517f84096431383f28c65f58a40a5b569aa504715a1d06d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.075711993398103,
  "max_drift_m": 10.075711993398103,
  "radial_IAE_m_s": 302.94224947726684,
  "signed_longitudinal_delta_m": -9.905725534054481,
  "tail_speed_mean_m_s": -0.1686994114534232,
  "tail_speed_rms_m_s": 0.16870517104472205,
  "tail_sensor_speed_mean_m_s": -0.1683757761851382,
  "tail_fk_speed_mean_m_s": -0.1683662176210468,
  "peak_tilt_rad": 0.021961642738272412,
  "peak_wheel_torque_nm": 2.7246317863464355,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.33386979997158
}
```
