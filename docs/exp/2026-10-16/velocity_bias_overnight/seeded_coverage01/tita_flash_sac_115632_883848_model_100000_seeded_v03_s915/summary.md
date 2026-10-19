# tita_flash_sac_115632_883848_model_100000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
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
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "be217a87fb84a66d16d6d82e9280833888271914ebf6ee1af306a9de72d6220d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09330662024694639,
  "max_drift_m": 0.11511224311928485,
  "radial_IAE_m_s": 5.401142032270241,
  "signed_longitudinal_delta_m": 0.09330639891175735,
  "tail_speed_mean_m_s": 9.294049400304876e-05,
  "tail_speed_rms_m_s": 9.297488243073687e-05,
  "tail_sensor_speed_mean_m_s": 9.25734398136585e-05,
  "tail_fk_speed_mean_m_s": 9.258138849428142e-05,
  "peak_tilt_rad": 0.08415648014772836,
  "peak_wheel_torque_nm": 0.49693766236305237,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5439966649418719,
  "final_integral_m_s": 0.5439966649418719,
  "elapsed_wall_s": 5.157646604988258
}
```
