# tita_flash_sac_193248_068255_model_100000_kick-0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_kick-0.2_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": -0.2,
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
  "initial_physics_sha256": "f0bf28588525daf2148e34a5a6f78096bc79dcd470f8d51f1091f935d5224cd5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023958155804464303,
  "max_drift_m": 0.04647071137353773,
  "radial_IAE_m_s": 1.4349407143596427,
  "signed_longitudinal_delta_m": 0.02395809528648242,
  "tail_speed_mean_m_s": 9.789089466791056e-06,
  "tail_speed_rms_m_s": 9.78919777000865e-06,
  "tail_sensor_speed_mean_m_s": 9.726761572805204e-06,
  "tail_fk_speed_mean_m_s": 9.74485529471526e-06,
  "peak_tilt_rad": 0.06396355056934233,
  "peak_wheel_torque_nm": 2.2217750549316406,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.262390676132184,
  "final_integral_m_s": 0.2623710825677305,
  "elapsed_wall_s": 4.344589531014208
}
```
