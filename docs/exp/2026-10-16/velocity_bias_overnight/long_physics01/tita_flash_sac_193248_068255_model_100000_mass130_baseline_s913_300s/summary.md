# tita_flash_sac_193248_068255_model_100000_mass130_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass130_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "c3aed3b8e5b46a84fbe61878a571bc5d459186a5f2ad09472d8ecd83d4b5fbaf",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 45.26044472054351,
  "max_drift_m": 45.26044472054351,
  "radial_IAE_m_s": 6931.292800792718,
  "signed_longitudinal_delta_m": -44.234818952234605,
  "tail_speed_mean_m_s": -0.14971708741557155,
  "tail_speed_rms_m_s": 0.15024931122835586,
  "tail_sensor_speed_mean_m_s": -0.1511546333658857,
  "tail_fk_speed_mean_m_s": -0.14918649628736125,
  "peak_tilt_rad": 0.06756440114689388,
  "peak_wheel_torque_nm": 4.236736297607422,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 24.53386537299957
}
```
