# tita_flash_sac_115632_883848_model_60000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
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
  "initial_physics_sha256": "b368a4c5d57079fecbed7746582aa3bf18c932345ef9c858891544d04d51c4f1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0024324912426833003,
  "max_drift_m": 0.00787421272544333,
  "radial_IAE_m_s": 0.17237396709445055,
  "signed_longitudinal_delta_m": 0.002406659442098428,
  "tail_speed_mean_m_s": -2.0604431870608975e-05,
  "tail_speed_rms_m_s": 2.151963744890765e-05,
  "tail_sensor_speed_mean_m_s": -2.054733416181388e-05,
  "tail_fk_speed_mean_m_s": -1.847614739667631e-05,
  "peak_tilt_rad": 0.06903178416639832,
  "peak_wheel_torque_nm": 0.19183632731437683,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.047104779470278885,
  "final_integral_m_s": 0.047104779470278885,
  "elapsed_wall_s": 15.177408129966352
}
```
