# tita_flash_sac_193248_068255_model_65000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "59133426750840e7da8062b79df7202980b056fba999ab486c35d1b47d93e7bc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01677490737059015,
  "max_drift_m": 0.03423400883099413,
  "radial_IAE_m_s": 1.0904899654718823,
  "signed_longitudinal_delta_m": -0.01676511241641473,
  "tail_speed_mean_m_s": 3.505022046177943e-05,
  "tail_speed_rms_m_s": 3.505406051748145e-05,
  "tail_sensor_speed_mean_m_s": 3.448907342311455e-05,
  "tail_fk_speed_mean_m_s": 3.5925831966076434e-05,
  "peak_tilt_rad": 0.048573446531664954,
  "peak_wheel_torque_nm": 0.23522041738033295,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18907486715155356,
  "final_integral_m_s": -0.18907486715155356,
  "elapsed_wall_s": 12.190939121996053
}
```
