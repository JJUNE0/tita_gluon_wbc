# tita_flash_sac_115632_883848_model_60000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
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
  "initial_physics_sha256": "e26f4510ef6942b9fde0f0e576b40389a67c607638fbd99a8396c1373992e70a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0020373272092553017,
  "max_drift_m": 0.03480668201002014,
  "radial_IAE_m_s": 0.1900263840694627,
  "signed_longitudinal_delta_m": 0.0020360541587357926,
  "tail_speed_mean_m_s": -1.7461795765930775e-05,
  "tail_speed_rms_m_s": 2.421674357399286e-05,
  "tail_sensor_speed_mean_m_s": -1.7076534025577184e-05,
  "tail_fk_speed_mean_m_s": -1.6177827342130136e-05,
  "peak_tilt_rad": 0.11443955404454265,
  "peak_wheel_torque_nm": 0.6568170189857483,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2224565168296346,
  "final_integral_m_s": -0.2224565168296346,
  "elapsed_wall_s": 12.134715919033624
}
```
