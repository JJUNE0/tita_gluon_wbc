# tita_flash_sac_193248_068255_model_100000_com_plus5mm_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com_plus5mm_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "d7dba4ff0f4681826cabe48f9857e5d9f6b74944d7cb81c4a6c13588b4a60f6f",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.04010893379083554,
  "max_drift_m": 0.048767843625359006,
  "radial_IAE_m_s": 11.428556413396688,
  "signed_longitudinal_delta_m": 0.04010678912452319,
  "tail_speed_mean_m_s": 1.069188499362621e-05,
  "tail_speed_rms_m_s": 1.0702671625008448e-05,
  "tail_sensor_speed_mean_m_s": 1.059971877113147e-05,
  "tail_fk_speed_mean_m_s": 1.0705244011718243e-05,
  "peak_tilt_rad": 0.05639424780773372,
  "peak_wheel_torque_nm": 0.5259721279144287,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4063879369919961,
  "final_integral_m_s": 0.40636635206927746,
  "elapsed_wall_s": 30.9187116670073
}
```
