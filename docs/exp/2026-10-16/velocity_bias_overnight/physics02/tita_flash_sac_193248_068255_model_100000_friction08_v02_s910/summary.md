# tita_flash_sac_193248_068255_model_100000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "fb03fdb494b82804f6534db3aa3fa394b4489176ffaabf8c88a2a99fe63145be",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025724203896336027,
  "max_drift_m": 0.036002478525958816,
  "radial_IAE_m_s": 1.5383508968839334,
  "signed_longitudinal_delta_m": 0.02572339942848561,
  "tail_speed_mean_m_s": 7.325528320632929e-06,
  "tail_speed_rms_m_s": 7.326260458294248e-06,
  "tail_sensor_speed_mean_m_s": 7.248422677180978e-06,
  "tail_fk_speed_mean_m_s": 7.3110229424290726e-06,
  "peak_tilt_rad": 0.051749317820376506,
  "peak_wheel_torque_nm": 0.5544223189353943,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.25857341287071367,
  "final_integral_m_s": 0.2585584372395767,
  "elapsed_wall_s": 15.966335028002504
}
```
