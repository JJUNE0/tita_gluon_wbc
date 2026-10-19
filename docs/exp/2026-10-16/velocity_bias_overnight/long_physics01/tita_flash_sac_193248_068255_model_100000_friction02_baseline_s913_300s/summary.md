# tita_flash_sac_193248_068255_model_100000_friction02_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction02_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "570f9044bef59c7dfba3e15c6bab225a85583fefd9ad32f5380b5c3cc61d94a4",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 20.680647018114257,
  "max_drift_m": 20.680647018114257,
  "radial_IAE_m_s": 3119.2593646433143,
  "signed_longitudinal_delta_m": 20.591894527909293,
  "tail_speed_mean_m_s": 0.06894656898823534,
  "tail_speed_rms_m_s": 0.06894656973890792,
  "tail_sensor_speed_mean_m_s": 0.06879725496622584,
  "tail_fk_speed_mean_m_s": 0.0687971078783017,
  "peak_tilt_rad": 0.053150136357132505,
  "peak_wheel_torque_nm": 0.3706170320510864,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 23.128975673986133
}
```
