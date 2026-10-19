# tita_flash_sac_193248_068255_model_100000_nominal_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_nominal_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "8d6dd1a7bfb6a1956a748aebab6fb9a983f6b57cd689cea7e1f1c27e864e911c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.165004707196239,
  "max_drift_m": 4.165004707196239,
  "radial_IAE_m_s": 125.86999878643812,
  "signed_longitudinal_delta_m": 4.164567134143618,
  "tail_speed_mean_m_s": 0.06846802318831856,
  "tail_speed_rms_m_s": 0.0684681554713274,
  "tail_sensor_speed_mean_m_s": 0.06832012825830751,
  "tail_fk_speed_mean_m_s": 0.06832038008120414,
  "peak_tilt_rad": 0.05235172541580968,
  "peak_wheel_torque_nm": 0.025886058807373047,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.717649697035085
}
```
