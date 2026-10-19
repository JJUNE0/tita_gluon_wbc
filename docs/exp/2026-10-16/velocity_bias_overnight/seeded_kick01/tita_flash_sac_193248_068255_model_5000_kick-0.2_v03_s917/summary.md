# tita_flash_sac_193248_068255_model_5000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "633ee4c84aaa496e93975613040a38c276af6089eb79af530f8869ba4dfebf14",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.1781394909496025,
  "max_drift_m": 0.17999670248481525,
  "radial_IAE_m_s": 10.483686323053387,
  "signed_longitudinal_delta_m": -0.17812724744414993,
  "tail_speed_mean_m_s": 3.720574261374668e-05,
  "tail_speed_rms_m_s": 3.722547278122786e-05,
  "tail_sensor_speed_mean_m_s": 3.206690774894396e-05,
  "tail_fk_speed_mean_m_s": 2.6295214528008034e-05,
  "peak_tilt_rad": 0.08612867205540287,
  "peak_wheel_torque_nm": 4.678239822387695,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0137340229090108,
  "final_integral_m_s": -1.0137340229090108,
  "elapsed_wall_s": 10.45956217002822
}
```
