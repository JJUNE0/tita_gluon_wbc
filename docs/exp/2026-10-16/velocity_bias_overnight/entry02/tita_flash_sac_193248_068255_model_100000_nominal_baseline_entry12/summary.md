# tita_flash_sac_193248_068255_model_100000_nominal_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_nominal_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
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
  "initial_physics_sha256": "71fd632d7de2d6df53bf5fdff4d65aab1bedf33412e6b4a1f09fad3449cb5241",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.16329596089265,
  "max_drift_m": 4.16329596089265,
  "radial_IAE_m_s": 125.2850474645695,
  "signed_longitudinal_delta_m": 4.1631316353665495,
  "tail_speed_mean_m_s": 0.06866573928692955,
  "tail_speed_rms_m_s": 0.06866607932995529,
  "tail_sensor_speed_mean_m_s": 0.0685174310622293,
  "tail_fk_speed_mean_m_s": 0.06851775470124753,
  "peak_tilt_rad": 0.052396947434310004,
  "peak_wheel_torque_nm": 0.6103775501251221,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.234510887996294
}
```
