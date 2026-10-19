# tita_flash_sac_193248_068255_model_100000_mass1.30_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass1.30_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "fc5b653bdeec2abe0b1b6b7479a213d8b7e5d3ed1394fa821770d3adaa066b37",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07913922510465889,
  "max_drift_m": 0.08160595048680928,
  "radial_IAE_m_s": 3.4365191801476023,
  "signed_longitudinal_delta_m": -0.07912231981635805,
  "tail_speed_mean_m_s": -0.0007121029389512654,
  "tail_speed_rms_m_s": 0.017597922156980562,
  "tail_sensor_speed_mean_m_s": 0.0009850442905205857,
  "tail_fk_speed_mean_m_s": -3.2240851248407005e-05,
  "peak_tilt_rad": 0.1606543617915026,
  "peak_wheel_torque_nm": 5.1172380447387695,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.43814670500821973,
  "final_integral_m_s": -0.3775283761414497,
  "elapsed_wall_s": 5.395509498019237
}
```
