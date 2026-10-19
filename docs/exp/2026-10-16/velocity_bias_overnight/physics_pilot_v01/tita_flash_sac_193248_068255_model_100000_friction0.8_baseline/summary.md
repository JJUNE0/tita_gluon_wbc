# tita_flash_sac_193248_068255_model_100000_friction0.8_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction0.8_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "826c6721b62bb4009ee25555c90be2a1664e6f1f74394fb6f17b691e875ef373",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.19435897187926,
  "max_drift_m": 4.19435897187926,
  "radial_IAE_m_s": 126.80285404773547,
  "signed_longitudinal_delta_m": 4.1940857939448515,
  "tail_speed_mean_m_s": 0.06884267156422384,
  "tail_speed_rms_m_s": 0.06884313706717914,
  "tail_sensor_speed_mean_m_s": 0.06869395836901628,
  "tail_fk_speed_mean_m_s": 0.06869435054786029,
  "peak_tilt_rad": 0.0526897491938616,
  "peak_wheel_torque_nm": 0.026691555976867676,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.392167565005366
}
```
