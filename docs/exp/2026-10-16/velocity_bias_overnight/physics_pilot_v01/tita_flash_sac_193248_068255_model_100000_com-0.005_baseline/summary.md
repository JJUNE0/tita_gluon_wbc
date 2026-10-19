# tita_flash_sac_193248_068255_model_100000_com-0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com-0.005_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
    },
    "kick": 0.0,
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
  "initial_physics_sha256": "1c399982d6a99a6e69875d93044de2c33fa35a1e972c2ac4dfd229aaff3b46ec",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.4832111563685488,
  "max_drift_m": 1.4832111563685488,
  "radial_IAE_m_s": 44.459630154165666,
  "signed_longitudinal_delta_m": 1.4831555882489542,
  "tail_speed_mean_m_s": 0.0247902020082723,
  "tail_speed_rms_m_s": 0.024790495136756,
  "tail_sensor_speed_mean_m_s": 0.024736691381549995,
  "tail_fk_speed_mean_m_s": 0.02473667816049802,
  "peak_tilt_rad": 0.045388689550364125,
  "peak_wheel_torque_nm": 0.027712002396583557,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.412590524996631
}
```
