# tita_flash_sac_193248_068255_model_5000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "fb5a6fed666a4c91ced872392b7affd960f9bcfd9d14b634ddb34ab0120764d5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.5204227456142632,
  "max_drift_m": 1.6509906364107372,
  "radial_IAE_m_s": 68.75240276766678,
  "signed_longitudinal_delta_m": -0.15788209158777555,
  "tail_speed_mean_m_s": -0.0448763385172541,
  "tail_speed_rms_m_s": 0.044888344820193424,
  "tail_sensor_speed_mean_m_s": -0.04547833887487777,
  "tail_fk_speed_mean_m_s": -0.04583738449791968,
  "peak_tilt_rad": 0.08882407725652874,
  "peak_wheel_torque_nm": 4.629655838012695,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.598184850008693
}
```
