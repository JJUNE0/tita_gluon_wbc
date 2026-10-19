# tita_flash_sac_193248_068255_model_100000_friction02_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction02_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "37292635e426bcea01ebbd7b436bd41b20ecc4fb80e5289c98291723714d4f26",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.2451898897372216,
  "max_drift_m": 4.2451898897372216,
  "radial_IAE_m_s": 127.87307013955603,
  "signed_longitudinal_delta_m": 4.243594671693534,
  "tail_speed_mean_m_s": 0.06997165314828806,
  "tail_speed_rms_m_s": 0.06997200689025868,
  "tail_sensor_speed_mean_m_s": 0.06985168738382715,
  "tail_fk_speed_mean_m_s": 0.06985107064384669,
  "peak_tilt_rad": 0.053150124241440944,
  "peak_wheel_torque_nm": 0.3706292510032654,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.931988879980054
}
```
