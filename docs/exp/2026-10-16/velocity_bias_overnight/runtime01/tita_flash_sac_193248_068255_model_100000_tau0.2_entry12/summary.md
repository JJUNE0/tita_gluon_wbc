# tita_flash_sac_193248_068255_model_100000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "initial_physics_sha256": "31c4ca27fd40ea4496c33938e2fe1ccaa46dcfb3324c4f8a0364da2400182664",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.026022264312005727,
  "max_drift_m": 0.03945816079941319,
  "radial_IAE_m_s": 1.5508044228572846,
  "signed_longitudinal_delta_m": 0.026021656360041102,
  "tail_speed_mean_m_s": 9.70125267138574e-06,
  "tail_speed_rms_m_s": 9.701496218707903e-06,
  "tail_sensor_speed_mean_m_s": 9.635548225035335e-06,
  "tail_fk_speed_mean_m_s": 9.662476031855432e-06,
  "peak_tilt_rad": 0.0514948515600302,
  "peak_wheel_torque_nm": 0.5861776471138,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2612091574833064,
  "final_integral_m_s": 0.2611896667693808,
  "elapsed_wall_s": 17.115177269966807
}
```
