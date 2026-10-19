# tita_flash_sac_193248_068255_model_100000_kick+0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_kick+0.2_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.2,
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
  "initial_physics_sha256": "06e527cb12e931d3fdbe3c946bcff7f64ffd581b53e30a1e593dae04e40712c8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.43315647706927,
  "max_drift_m": 4.43315647706927,
  "radial_IAE_m_s": 141.85229069994256,
  "signed_longitudinal_delta_m": 4.433051765463748,
  "tail_speed_mean_m_s": 0.06838518658648886,
  "tail_speed_rms_m_s": 0.06838523817811917,
  "tail_sensor_speed_mean_m_s": 0.06823749269981082,
  "tail_fk_speed_mean_m_s": 0.06823766363440656,
  "peak_tilt_rad": 0.0719609564536654,
  "peak_wheel_torque_nm": 1.314058780670166,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.256640283041634
}
```
