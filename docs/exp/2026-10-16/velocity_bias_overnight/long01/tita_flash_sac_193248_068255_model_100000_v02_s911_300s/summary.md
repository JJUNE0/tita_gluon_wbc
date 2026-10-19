# tita_flash_sac_193248_068255_model_100000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
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
  "initial_physics_sha256": "72a54c1f26adda82fe4adec9d1893f3dae684c2ad348c45e027212ae770ae85e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.028566341471666853,
  "max_drift_m": 0.036146399716256945,
  "radial_IAE_m_s": 8.091015421431562,
  "signed_longitudinal_delta_m": 0.02856593956707071,
  "tail_speed_mean_m_s": 4.120677269151217e-06,
  "tail_speed_rms_m_s": 5.405895575443555e-06,
  "tail_sensor_speed_mean_m_s": 4.106945370897092e-06,
  "tail_fk_speed_mean_m_s": 4.08655883330157e-06,
  "peak_tilt_rad": 0.051494853480437364,
  "peak_wheel_torque_nm": 0.5732324719429016,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.28652289705470035,
  "final_integral_m_s": 0.28651788694542263,
  "elapsed_wall_s": 73.41225165303331
}
```
