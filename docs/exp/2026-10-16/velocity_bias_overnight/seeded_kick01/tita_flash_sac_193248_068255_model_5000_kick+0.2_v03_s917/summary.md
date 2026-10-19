# tita_flash_sac_193248_068255_model_5000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "fb5a6fed666a4c91ced872392b7affd960f9bcfd9d14b634ddb34ab0120764d5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.17522539866639036,
  "max_drift_m": 0.17692925116825184,
  "radial_IAE_m_s": 9.937001009859408,
  "signed_longitudinal_delta_m": -0.17516800211749037,
  "tail_speed_mean_m_s": 3.7113024035574944e-05,
  "tail_speed_rms_m_s": 3.7134781663122284e-05,
  "tail_sensor_speed_mean_m_s": 3.191978406586513e-05,
  "tail_fk_speed_mean_m_s": 2.613191414715261e-05,
  "peak_tilt_rad": 0.0752045597582085,
  "peak_wheel_torque_nm": 4.600150108337402,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0138071118628638,
  "final_integral_m_s": -1.0138071118628638,
  "elapsed_wall_s": 10.596543971973006
}
```
