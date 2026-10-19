# tita_flash_sac_193248_068255_model_90000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "ed1857a5c2b259adfdefc1431b42fece068fe2900bf9ca9c02d336450b06913e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09119567916980889,
  "max_drift_m": 0.1083720355491429,
  "radial_IAE_m_s": 5.130115487386533,
  "signed_longitudinal_delta_m": 0.09119542227916086,
  "tail_speed_mean_m_s": 0.00016840681854285948,
  "tail_speed_rms_m_s": 0.0001692913195771078,
  "tail_sensor_speed_mean_m_s": 0.00016826350656347564,
  "tail_fk_speed_mean_m_s": 0.00016967683861759502,
  "peak_tilt_rad": 0.10162931193458857,
  "peak_wheel_torque_nm": 1.6775009632110596,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6357020566378011,
  "final_integral_m_s": 0.6357020566378011,
  "elapsed_wall_s": 8.709521097014658
}
```
