# tita_flash_sac_193248_068255_model_100000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "3fedc11efdd40237efce752ca6e86656605aaef779bc0706c06652d5cae1d218",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 20.62152075776748,
  "max_drift_m": 20.62152075776748,
  "radial_IAE_m_s": 3097.778458348629,
  "signed_longitudinal_delta_m": 20.558969923832667,
  "tail_speed_mean_m_s": 0.06897341856520746,
  "tail_speed_rms_m_s": 0.06897341908846126,
  "tail_sensor_speed_mean_m_s": 0.06882405397232969,
  "tail_fk_speed_mean_m_s": 0.06882389745592195,
  "peak_tilt_rad": 0.05244008895028762,
  "peak_wheel_torque_nm": 0.608325719833374,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 18.8202661210089
}
```
