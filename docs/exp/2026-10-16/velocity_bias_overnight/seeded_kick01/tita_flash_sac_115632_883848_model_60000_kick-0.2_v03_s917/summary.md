# tita_flash_sac_115632_883848_model_60000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
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
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "82b38840161f009f085cc5bc7b97143f94203aff26571f5474187b78a331f37f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0005983168016949282,
  "max_drift_m": 0.08278754639838821,
  "radial_IAE_m_s": 0.18731127080113316,
  "signed_longitudinal_delta_m": 0.0002825161303748032,
  "tail_speed_mean_m_s": -2.4555113616610865e-05,
  "tail_speed_rms_m_s": 2.545988162485035e-05,
  "tail_sensor_speed_mean_m_s": -2.457974190378037e-05,
  "tail_fk_speed_mean_m_s": -2.2475297758753117e-05,
  "peak_tilt_rad": 0.09481207162012906,
  "peak_wheel_torque_nm": 1.5610913038253784,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04751167995414765,
  "final_integral_m_s": 0.04751167995414765,
  "elapsed_wall_s": 10.086946388008073
}
```
