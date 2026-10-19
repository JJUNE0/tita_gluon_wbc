# tita_flash_sac_193248_068255_model_100000_nominal_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_nominal_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "final_drift_m": 0.025351557052696278,
  "max_drift_m": 0.03819135205122653,
  "radial_IAE_m_s": 1.5128573794955629,
  "signed_longitudinal_delta_m": 0.02535040523077303,
  "tail_speed_mean_m_s": 9.797076703756141e-06,
  "tail_speed_rms_m_s": 9.797162571775198e-06,
  "tail_sensor_speed_mean_m_s": 9.734986988884565e-06,
  "tail_fk_speed_mean_m_s": 9.752253551775695e-06,
  "peak_tilt_rad": 0.05235172541580968,
  "peak_wheel_torque_nm": 0.648306131362915,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2625037986944976,
  "final_integral_m_s": 0.26248411692402734,
  "elapsed_wall_s": 4.713535900984425
}
```
