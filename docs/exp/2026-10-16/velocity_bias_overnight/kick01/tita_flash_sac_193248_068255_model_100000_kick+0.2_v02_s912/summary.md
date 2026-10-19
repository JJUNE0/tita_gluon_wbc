# tita_flash_sac_193248_068255_model_100000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "8e956813a556aabb4a4113dd90f7f969b16b63fac5d0480b51d6ab812816c169",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.027361771825874837,
  "max_drift_m": 0.10171582495252071,
  "radial_IAE_m_s": 1.659397810571559,
  "signed_longitudinal_delta_m": 0.027361364536711986,
  "tail_speed_mean_m_s": 9.747992224055551e-06,
  "tail_speed_rms_m_s": 9.748129504366287e-06,
  "tail_sensor_speed_mean_m_s": 9.684787329080849e-06,
  "tail_fk_speed_mean_m_s": 9.706565773501303e-06,
  "peak_tilt_rad": 0.10397707941378598,
  "peak_wheel_torque_nm": 1.449965000152588,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2772308007826468,
  "final_integral_m_s": 0.27721126287712,
  "elapsed_wall_s": 12.657529939024244
}
```
