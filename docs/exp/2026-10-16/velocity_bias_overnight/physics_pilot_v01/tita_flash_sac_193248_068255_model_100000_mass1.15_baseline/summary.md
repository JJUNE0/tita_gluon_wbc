# tita_flash_sac_193248_068255_model_100000_mass1.15_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass1.15_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "c104d86dfe462cb22f19f38678522b2d99ed775cef4084cce27eb15e9e1a1e91",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.719323449534021,
  "max_drift_m": 4.719323449534021,
  "radial_IAE_m_s": 141.38039093164969,
  "signed_longitudinal_delta_m": -4.7153310067023995,
  "tail_speed_mean_m_s": -0.07900218432863493,
  "tail_speed_rms_m_s": 0.0790023330727605,
  "tail_sensor_speed_mean_m_s": -0.07885843134714143,
  "tail_fk_speed_mean_m_s": -0.07885804855404552,
  "peak_tilt_rad": 0.0532022151287701,
  "peak_wheel_torque_nm": 0.08826488256454468,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.447245939983986
}
```
