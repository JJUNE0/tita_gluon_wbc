# tita_flash_sac_193248_068255_model_100000_friction08_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction08_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "db2dbec7e7fe58c17311acc64866191cd36a62e0163b28519363c794d6121e49",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 20.647254814572317,
  "max_drift_m": 20.647254814572317,
  "radial_IAE_m_s": 3105.1862609855393,
  "signed_longitudinal_delta_m": 20.63359205075413,
  "tail_speed_mean_m_s": 0.06896171319226349,
  "tail_speed_rms_m_s": 0.06896171381820157,
  "tail_sensor_speed_mean_m_s": 0.06881237420478323,
  "tail_fk_speed_mean_m_s": 0.06881221811811195,
  "peak_tilt_rad": 0.05276112918202425,
  "peak_wheel_torque_nm": 0.5884815454483032,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 22.363358003960457
}
```
