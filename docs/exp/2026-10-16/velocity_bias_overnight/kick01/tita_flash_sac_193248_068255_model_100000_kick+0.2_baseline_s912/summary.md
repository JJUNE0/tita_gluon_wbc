# tita_flash_sac_193248_068255_model_100000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "8e956813a556aabb4a4113dd90f7f969b16b63fac5d0480b51d6ab812816c169",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.428701041378502,
  "max_drift_m": 4.428701041378502,
  "radial_IAE_m_s": 141.159233678073,
  "signed_longitudinal_delta_m": 4.428693119320071,
  "tail_speed_mean_m_s": 0.06854121742626723,
  "tail_speed_rms_m_s": 0.06854143137179268,
  "tail_sensor_speed_mean_m_s": 0.06839320785328995,
  "tail_fk_speed_mean_m_s": 0.06839345172100787,
  "peak_tilt_rad": 0.06850478445385333,
  "peak_wheel_torque_nm": 0.7997398376464844,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.293740244000219
}
```
