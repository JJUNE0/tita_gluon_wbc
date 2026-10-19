# tita_flash_sac_193248_068255_model_5000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "c3502eb3b5cb6afc5d5c8926f720864d45be0511ebb977b000f1d15992fd390c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.3889164489463555,
  "max_drift_m": 1.4470033014030454,
  "radial_IAE_m_s": 59.35140403140731,
  "signed_longitudinal_delta_m": 0.0772690229428584,
  "tail_speed_mean_m_s": -0.04054745644948435,
  "tail_speed_rms_m_s": 0.04055215077279479,
  "tail_sensor_speed_mean_m_s": -0.04113117940711794,
  "tail_fk_speed_mean_m_s": -0.04145003573265441,
  "peak_tilt_rad": 0.0786831705026112,
  "peak_wheel_torque_nm": 0.8600480556488037,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.029205502010882
}
```
