# tita_flash_sac_193248_068255_model_100000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "fb03fdb494b82804f6534db3aa3fa394b4489176ffaabf8c88a2a99fe63145be",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.193149357245256,
  "max_drift_m": 4.193149357245256,
  "radial_IAE_m_s": 126.18477115203922,
  "signed_longitudinal_delta_m": 4.191783891949355,
  "tail_speed_mean_m_s": 0.06913331056783922,
  "tail_speed_rms_m_s": 0.06913391751833078,
  "tail_sensor_speed_mean_m_s": 0.06898395743265309,
  "tail_fk_speed_mean_m_s": 0.06898439583992179,
  "peak_tilt_rad": 0.05273626686684563,
  "peak_wheel_torque_nm": 0.5889357924461365,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 17.61647087399615
}
```
