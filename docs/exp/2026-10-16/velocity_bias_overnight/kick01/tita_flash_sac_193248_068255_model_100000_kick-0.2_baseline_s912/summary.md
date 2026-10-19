# tita_flash_sac_193248_068255_model_100000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "918af4d17ed1b8a9579cc3c67e0280e711a68d79093ee0dc9a8145076f10c662",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.9002091389294344,
  "max_drift_m": 3.9002091389294344,
  "radial_IAE_m_s": 110.1444598829934,
  "signed_longitudinal_delta_m": 3.899855750389742,
  "tail_speed_mean_m_s": 0.06874694744132859,
  "tail_speed_rms_m_s": 0.06874735630185555,
  "tail_sensor_speed_mean_m_s": 0.06859846409852845,
  "tail_fk_speed_mean_m_s": 0.0685988095531696,
  "peak_tilt_rad": 0.052360077965903695,
  "peak_wheel_torque_nm": 2.430337429046631,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.340824606013484
}
```
