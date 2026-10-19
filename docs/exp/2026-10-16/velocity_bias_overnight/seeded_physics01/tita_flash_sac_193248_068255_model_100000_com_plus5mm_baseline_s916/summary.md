# tita_flash_sac_193248_068255_model_100000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a",
  "onnx_sha256": "fcd7b62b26d94ec01f945f05940b24a521d0ed55477b8dfa4b0e93c3af756a6c",
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
  "initial_physics_sha256": "1a0fde90b6cd50eac5533d07969e79bc73239e65251c3cda979838e234fc6a61",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.1917169182863026,
  "max_drift_m": 7.1917169182863026,
  "radial_IAE_m_s": 214.38559993863316,
  "signed_longitudinal_delta_m": 7.19118311223086,
  "tail_speed_mean_m_s": 0.12059698672503581,
  "tail_speed_rms_m_s": 0.12059699695511936,
  "tail_sensor_speed_mean_m_s": 0.1203361542524831,
  "tail_fk_speed_mean_m_s": 0.12033638589489305,
  "peak_tilt_rad": 0.05701900360476775,
  "peak_wheel_torque_nm": 0.601912260055542,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.291797695972491
}
```
