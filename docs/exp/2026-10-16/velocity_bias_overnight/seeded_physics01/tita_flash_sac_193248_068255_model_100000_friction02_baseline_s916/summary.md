# tita_flash_sac_193248_068255_model_100000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "6b960244f094b60c41278fa63230684b1ad957fc9d50a4073ead9720dae9d806",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.245189526716182,
  "max_drift_m": 4.245189526716182,
  "radial_IAE_m_s": 127.87305149009264,
  "signed_longitudinal_delta_m": 4.243594337897589,
  "tail_speed_mean_m_s": 0.06997166697199894,
  "tail_speed_rms_m_s": 0.06997202068335669,
  "tail_sensor_speed_mean_m_s": 0.06985170107374192,
  "tail_fk_speed_mean_m_s": 0.06985108453260393,
  "peak_tilt_rad": 0.0531501001110497,
  "peak_wheel_torque_nm": 0.37062597274780273,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.642205685027875
}
```
