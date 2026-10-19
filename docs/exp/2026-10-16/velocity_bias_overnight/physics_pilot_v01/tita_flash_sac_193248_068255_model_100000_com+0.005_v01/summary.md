# tita_flash_sac_193248_068255_model_100000_com+0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com+0.005_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "9d9964c43ab85806b8b7e2ece8670237fc0f132aa566d6b26b394c7dea993c19",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.035753306785232086,
  "max_drift_m": 0.05133243998698349,
  "radial_IAE_m_s": 2.1060431990069297,
  "signed_longitudinal_delta_m": 0.035752306322967935,
  "tail_speed_mean_m_s": 3.362330558623072e-05,
  "tail_speed_rms_m_s": 3.362452699342055e-05,
  "tail_sensor_speed_mean_m_s": 3.3313221135901675e-05,
  "tail_fk_speed_mean_m_s": 3.360091527060922e-05,
  "peak_tilt_rad": 0.05712046708731844,
  "peak_wheel_torque_nm": 0.8680722713470459,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.37294329551305205,
  "final_integral_m_s": 0.3728767831829634,
  "elapsed_wall_s": 5.445774562016595
}
```
