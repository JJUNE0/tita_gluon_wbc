# tita_flash_sac_193248_068255_model_100000_friction0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction0.2_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.2
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "2efcdf094a72e333360fba0ebd03acb0a266843d844b7285e5804ace1d0e4935",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02792669686537877,
  "max_drift_m": 0.03947418213250118,
  "radial_IAE_m_s": 1.6571820023272938,
  "signed_longitudinal_delta_m": 0.027923206398299278,
  "tail_speed_mean_m_s": 1.4395866894765108e-05,
  "tail_speed_rms_m_s": 1.4434896650041582e-05,
  "tail_sensor_speed_mean_m_s": 1.4369857310204994e-05,
  "tail_fk_speed_mean_m_s": 1.4319317653339443e-05,
  "peak_tilt_rad": 0.0530826196775096,
  "peak_wheel_torque_nm": 0.9036199450492859,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.28259253588426153,
  "final_integral_m_s": 0.2825663382441917,
  "elapsed_wall_s": 5.399882661993615
}
```
