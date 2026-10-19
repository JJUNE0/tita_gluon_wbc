# tita_flash_sac_193248_068255_model_100000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "8e267593f21070b18956956a02fdebd2a07d99c41db6acf178eccb105ed1fd1e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07269198375033507,
  "max_drift_m": 0.07533253474856451,
  "radial_IAE_m_s": 3.2669290958285124,
  "signed_longitudinal_delta_m": -0.07268952778090682,
  "tail_speed_mean_m_s": -0.0005266736903423834,
  "tail_speed_rms_m_s": 0.016434515765271725,
  "tail_sensor_speed_mean_m_s": 0.0023991126578756265,
  "tail_fk_speed_mean_m_s": 5.248662136486033e-05,
  "peak_tilt_rad": 0.15111887179873928,
  "peak_wheel_torque_nm": 4.638599395751953,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.36559942970426657,
  "final_integral_m_s": -0.36769234073315243,
  "elapsed_wall_s": 26.42202960595023
}
```
