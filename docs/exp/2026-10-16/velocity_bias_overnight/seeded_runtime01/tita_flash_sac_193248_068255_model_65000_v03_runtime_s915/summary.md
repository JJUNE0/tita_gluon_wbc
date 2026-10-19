# tita_flash_sac_193248_068255_model_65000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "2812515b8fa1568a255d04c28f0634c8f408b9fd7375bc0ae01b9ea4238dfde6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01597565706007547,
  "max_drift_m": 0.033078813850961356,
  "radial_IAE_m_s": 1.0362704368543842,
  "signed_longitudinal_delta_m": -0.015966679592291484,
  "tail_speed_mean_m_s": 3.1440880345894155e-05,
  "tail_speed_rms_m_s": 3.1444827113211525e-05,
  "tail_sensor_speed_mean_m_s": 3.1021748410795664e-05,
  "tail_fk_speed_mean_m_s": 3.2342869379294266e-05,
  "peak_tilt_rad": 0.04795470998483253,
  "peak_wheel_torque_nm": 0.22586306929588318,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18367152951356128,
  "final_integral_m_s": -0.18367152951356128,
  "elapsed_wall_s": 16.19307158899028
}
```
