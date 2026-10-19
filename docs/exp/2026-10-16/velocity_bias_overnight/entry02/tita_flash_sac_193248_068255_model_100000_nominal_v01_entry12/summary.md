# tita_flash_sac_193248_068255_model_100000_nominal_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_nominal_v01_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "71fd632d7de2d6df53bf5fdff4d65aab1bedf33412e6b4a1f09fad3449cb5241",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.026020666729750057,
  "max_drift_m": 0.034881512971166324,
  "radial_IAE_m_s": 1.5481950006299616,
  "signed_longitudinal_delta_m": 0.02602004268117718,
  "tail_speed_mean_m_s": 9.695543943904219e-06,
  "tail_speed_rms_m_s": 9.695760562062473e-06,
  "tail_sensor_speed_mean_m_s": 9.630027215889008e-06,
  "tail_fk_speed_mean_m_s": 9.656990355111338e-06,
  "peak_tilt_rad": 0.05149485130399323,
  "peak_wheel_torque_nm": 0.5636703968048096,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2612000541291352,
  "final_integral_m_s": 0.26118062451389507,
  "elapsed_wall_s": 4.713221442012582
}
```
