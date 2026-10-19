# tita_flash_sac_193248_068255_model_65000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 2.6464070870579057,
  "max_drift_m": 2.6464070870579057,
  "radial_IAE_m_s": 80.05478377282793,
  "signed_longitudinal_delta_m": -2.6434504302975146,
  "tail_speed_mean_m_s": -0.04329471775728516,
  "tail_speed_rms_m_s": 0.043295328090520495,
  "tail_sensor_speed_mean_m_s": -0.04320945257634916,
  "tail_fk_speed_mean_m_s": -0.04320469559455398,
  "peak_tilt_rad": 0.029539268782760475,
  "peak_wheel_torque_nm": 0.049872949719429016,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.158568092971109
}
```
