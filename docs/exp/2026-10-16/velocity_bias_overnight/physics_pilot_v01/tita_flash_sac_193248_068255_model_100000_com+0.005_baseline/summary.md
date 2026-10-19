# tita_flash_sac_193248_068255_model_100000_com+0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com+0.005_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "9d9964c43ab85806b8b7e2ece8670237fc0f132aa566d6b26b394c7dea993c19",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.238281823236472,
  "max_drift_m": 7.238281823236472,
  "radial_IAE_m_s": 217.10894925835692,
  "signed_longitudinal_delta_m": 7.237898107811611,
  "tail_speed_mean_m_s": 0.12059839453089272,
  "tail_speed_rms_m_s": 0.12059840436219625,
  "tail_sensor_speed_mean_m_s": 0.12033754669612494,
  "tail_fk_speed_mean_m_s": 0.12033779533863978,
  "peak_tilt_rad": 0.0571205555850236,
  "peak_wheel_torque_nm": 0.03319162130355835,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.469704009999987
}
```
