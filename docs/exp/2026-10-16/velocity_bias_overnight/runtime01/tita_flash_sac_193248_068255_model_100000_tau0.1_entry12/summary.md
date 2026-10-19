# tita_flash_sac_193248_068255_model_100000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "31c4ca27fd40ea4496c33938e2fe1ccaa46dcfb3324c4f8a0364da2400182664",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.026021062929553588,
  "max_drift_m": 0.036146414976396576,
  "radial_IAE_m_s": 1.5490758358306604,
  "signed_longitudinal_delta_m": 0.026020442408390503,
  "tail_speed_mean_m_s": 9.696967426317534e-06,
  "tail_speed_rms_m_s": 9.697181876024384e-06,
  "tail_sensor_speed_mean_m_s": 9.63195735452258e-06,
  "tail_fk_speed_mean_m_s": 9.658372764022245e-06,
  "peak_tilt_rad": 0.0514948515600302,
  "peak_wheel_torque_nm": 0.5732364654541016,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.26120289915378525,
  "final_integral_m_s": 0.26118340534941514,
  "elapsed_wall_s": 14.813672256015707
}
```
