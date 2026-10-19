# tita_flash_sac_193248_068255_model_100000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "02eee71f06bad406f72f5570dfddf16b996bfcb0182fc3302c27655f5328b4b5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.035916925576251126,
  "max_drift_m": 0.04881176280794299,
  "radial_IAE_m_s": 2.134626231467139,
  "signed_longitudinal_delta_m": 0.03591587297722207,
  "tail_speed_mean_m_s": 1.5001114948481973e-05,
  "tail_speed_rms_m_s": 1.606782694733786e-05,
  "tail_sensor_speed_mean_m_s": 1.477731323711462e-05,
  "tail_fk_speed_mean_m_s": 1.5010078164768564e-05,
  "peak_tilt_rad": 0.05653267062277312,
  "peak_wheel_torque_nm": 0.5225400328636169,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.36460159026869626,
  "final_integral_m_s": 0.3645832400213813,
  "elapsed_wall_s": 25.57750648900401
}
```
