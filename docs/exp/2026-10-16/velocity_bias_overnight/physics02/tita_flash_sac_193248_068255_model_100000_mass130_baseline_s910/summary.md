# tita_flash_sac_193248_068255_model_100000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a",
  "onnx_sha256": "fcd7b62b26d94ec01f945f05940b24a521d0ed55477b8dfa4b0e93c3af756a6c",
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
  "initial_physics_sha256": "8e267593f21070b18956956a02fdebd2a07d99c41db6acf178eccb105ed1fd1e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.489325920811423,
  "max_drift_m": 9.489325920811423,
  "radial_IAE_m_s": 285.71584931565235,
  "signed_longitudinal_delta_m": -9.482096632670844,
  "tail_speed_mean_m_s": -0.15694367456834554,
  "tail_speed_rms_m_s": 0.1573508926877128,
  "tail_sensor_speed_mean_m_s": -0.15685728673989477,
  "tail_fk_speed_mean_m_s": -0.15644533909868336,
  "peak_tilt_rad": 0.06756433987899224,
  "peak_wheel_torque_nm": 3.906966209411621,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 18.084026264958084
}
```
