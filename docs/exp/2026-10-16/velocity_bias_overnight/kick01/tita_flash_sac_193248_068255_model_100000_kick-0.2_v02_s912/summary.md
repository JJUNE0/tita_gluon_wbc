# tita_flash_sac_193248_068255_model_100000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "918af4d17ed1b8a9579cc3c67e0280e711a68d79093ee0dc9a8145076f10c662",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024605809013461613,
  "max_drift_m": 0.05365299948488535,
  "radial_IAE_m_s": 1.4838055713460532,
  "signed_longitudinal_delta_m": 0.024605417893906918,
  "tail_speed_mean_m_s": 9.690968637303475e-06,
  "tail_speed_rms_m_s": 9.691241291977188e-06,
  "tail_sensor_speed_mean_m_s": 9.625318080339178e-06,
  "tail_fk_speed_mean_m_s": 9.652547446806688e-06,
  "peak_tilt_rad": 0.07070552360468962,
  "peak_wheel_torque_nm": 2.633742094039917,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.27659071180765143,
  "final_integral_m_s": 0.27657122644027,
  "elapsed_wall_s": 12.62735425698338
}
```
