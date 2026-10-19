# tita_flash_sac_193248_068255_model_100000_friction0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction0.2_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "2efcdf094a72e333360fba0ebd03acb0a266843d844b7285e5804ace1d0e4935",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.242435581972499,
  "max_drift_m": 4.242435581972499,
  "radial_IAE_m_s": 128.3046286286121,
  "signed_longitudinal_delta_m": 4.242423156528531,
  "tail_speed_mean_m_s": 0.06970737550784704,
  "tail_speed_rms_m_s": 0.06970774443122824,
  "tail_sensor_speed_mean_m_s": 0.06958422433489796,
  "tail_fk_speed_mean_m_s": 0.06958361582681326,
  "peak_tilt_rad": 0.0530826196775096,
  "peak_wheel_torque_nm": 0.022978901863098145,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.470252780010924
}
```
