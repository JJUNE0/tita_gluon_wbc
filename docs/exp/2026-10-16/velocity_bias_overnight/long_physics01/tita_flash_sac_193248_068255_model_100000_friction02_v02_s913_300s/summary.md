# tita_flash_sac_193248_068255_model_100000_friction02_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction02_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
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
  "initial_physics_sha256": "570f9044bef59c7dfba3e15c6bab225a85583fefd9ad32f5380b5c3cc61d94a4",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.029437710006918714,
  "max_drift_m": 0.037591237291370865,
  "radial_IAE_m_s": 8.497295403630401,
  "signed_longitudinal_delta_m": 0.029430286780366043,
  "tail_speed_mean_m_s": 1.0765884093234183e-05,
  "tail_speed_rms_m_s": 1.0772772396944264e-05,
  "tail_sensor_speed_mean_m_s": 1.0689731056010674e-05,
  "tail_fk_speed_mean_m_s": 1.074039375857337e-05,
  "peak_tilt_rad": 0.05249847281096054,
  "peak_wheel_torque_nm": 0.6505957841873169,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2946860122909478,
  "final_integral_m_s": 0.29466453731605674,
  "elapsed_wall_s": 29.535476740973536
}
```
