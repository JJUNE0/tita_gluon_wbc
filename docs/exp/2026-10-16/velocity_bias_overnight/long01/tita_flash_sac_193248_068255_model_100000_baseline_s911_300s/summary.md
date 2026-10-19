# tita_flash_sac_193248_068255_model_100000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "72a54c1f26adda82fe4adec9d1893f3dae684c2ad348c45e027212ae770ae85e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 20.617638311648182,
  "max_drift_m": 20.617638311648182,
  "radial_IAE_m_s": 3096.5991245565665,
  "signed_longitudinal_delta_m": 20.551573369770004,
  "tail_speed_mean_m_s": 0.0689749606786337,
  "tail_speed_rms_m_s": 0.06897496119576509,
  "tail_sensor_speed_mean_m_s": 0.06882559262151958,
  "tail_fk_speed_mean_m_s": 0.06882543636323687,
  "peak_tilt_rad": 0.05239693996976236,
  "peak_wheel_torque_nm": 0.6103731989860535,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 57.45675810298417
}
```
