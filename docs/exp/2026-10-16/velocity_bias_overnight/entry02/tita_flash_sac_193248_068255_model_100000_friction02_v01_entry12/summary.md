# tita_flash_sac_193248_068255_model_100000_friction02_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction02_v01_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "initial_physics_sha256": "37292635e426bcea01ebbd7b436bd41b20ecc4fb80e5289c98291723714d4f26",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02734458326412037,
  "max_drift_m": 0.0362802598601993,
  "radial_IAE_m_s": 1.6281538032018188,
  "signed_longitudinal_delta_m": 0.027341672647493966,
  "tail_speed_mean_m_s": 8.612529185043192e-06,
  "tail_speed_rms_m_s": 8.702957923347157e-06,
  "tail_sensor_speed_mean_m_s": 8.619523881579434e-06,
  "tail_fk_speed_mean_m_s": 8.541087573245088e-06,
  "peak_tilt_rad": 0.05249294920287784,
  "peak_wheel_torque_nm": 0.7223513126373291,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.273517156356107,
  "final_integral_m_s": 0.27349785954165345,
  "elapsed_wall_s": 6.931264353974257
}
```
