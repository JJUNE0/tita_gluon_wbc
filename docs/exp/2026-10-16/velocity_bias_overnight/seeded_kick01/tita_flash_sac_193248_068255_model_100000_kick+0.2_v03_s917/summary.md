# tita_flash_sac_193248_068255_model_100000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "5eaafb61841d9808f19644aadaa9b1fcea3ded28cfe48b829f166c8370ed5d45",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03004701188376957,
  "max_drift_m": 0.10338524589497412,
  "radial_IAE_m_s": 1.967672666009355,
  "signed_longitudinal_delta_m": -0.030044942673986646,
  "tail_speed_mean_m_s": 2.429801216590631e-05,
  "tail_speed_rms_m_s": 2.4298276934666605e-05,
  "tail_sensor_speed_mean_m_s": 2.4202602950399674e-05,
  "tail_fk_speed_mean_m_s": 2.4226532741159053e-05,
  "peak_tilt_rad": 0.06663376995818537,
  "peak_wheel_torque_nm": 1.4810137748718262,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.261487832287449,
  "final_integral_m_s": 0.261487832287449,
  "elapsed_wall_s": 10.457184174039867
}
```
