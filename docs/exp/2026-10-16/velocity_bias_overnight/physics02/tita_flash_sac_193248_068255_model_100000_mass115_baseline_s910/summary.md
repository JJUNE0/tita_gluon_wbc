# tita_flash_sac_193248_068255_model_100000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "18ea42bd541312db844ebcdbff9461c9eeeb23f02076d4751af0f7aa193f9461",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.667229622986081,
  "max_drift_m": 4.667229622986081,
  "radial_IAE_m_s": 138.86721454906876,
  "signed_longitudinal_delta_m": -4.665748810163007,
  "tail_speed_mean_m_s": -0.07850502781338675,
  "tail_speed_rms_m_s": 0.07850503008726184,
  "tail_sensor_speed_mean_m_s": -0.07834403063678055,
  "tail_fk_speed_mean_m_s": -0.0783438443310139,
  "peak_tilt_rad": 0.06175375322513088,
  "peak_wheel_torque_nm": 1.4359790086746216,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.030808940005954
}
```
