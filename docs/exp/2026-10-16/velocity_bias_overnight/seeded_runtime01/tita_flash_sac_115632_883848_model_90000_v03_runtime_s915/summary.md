# tita_flash_sac_115632_883848_model_90000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "009fc58416ba0b6033ef41fede0b5d890768095ac13b1f983eb66aa2d812706b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04521633527717743,
  "max_drift_m": 0.059603474724429055,
  "radial_IAE_m_s": 2.5465939666357302,
  "signed_longitudinal_delta_m": 0.04521502664830036,
  "tail_speed_mean_m_s": 9.878878704545801e-05,
  "tail_speed_rms_m_s": 0.00010034077610237711,
  "tail_sensor_speed_mean_m_s": 9.830757252637534e-05,
  "tail_fk_speed_mean_m_s": 9.944642640814196e-05,
  "peak_tilt_rad": 0.06862651366306216,
  "peak_wheel_torque_nm": 0.4226071834564209,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.39265878311876384,
  "final_integral_m_s": 0.39265878311876384,
  "elapsed_wall_s": 13.401215924997814
}
```
