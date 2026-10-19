# tita_flash_sac_193248_068255_model_100000_kick-0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_kick-0.2_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": -0.2,
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
  "initial_physics_sha256": "f0bf28588525daf2148e34a5a6f78096bc79dcd470f8d51f1091f935d5224cd5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.904029844679045,
  "max_drift_m": 3.904029844679045,
  "radial_IAE_m_s": 110.75947446512045,
  "signed_longitudinal_delta_m": 3.9034208674882716,
  "tail_speed_mean_m_s": 0.06852586482737738,
  "tail_speed_rms_m_s": 0.06852606244905997,
  "tail_sensor_speed_mean_m_s": 0.06837789844542477,
  "tail_fk_speed_mean_m_s": 0.06837812513362536,
  "peak_tilt_rad": 0.05235172541580968,
  "peak_wheel_torque_nm": 1.861321210861206,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.535062053997535
}
```
