# tita_flash_sac_193248_068255_model_100000_com_plus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com_plus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "d7dba4ff0f4681826cabe48f9857e5d9f6b74944d7cb81c4a6c13588b4a60f6f",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 36.128706160269815,
  "max_drift_m": 36.128706160269815,
  "radial_IAE_m_s": 5413.2862902039205,
  "signed_longitudinal_delta_m": 36.01996290795377,
  "tail_speed_mean_m_s": 0.12091692892661846,
  "tail_speed_rms_m_s": 0.12091692900965818,
  "tail_sensor_speed_mean_m_s": 0.12065507410048809,
  "tail_fk_speed_mean_m_s": 0.12065500132073896,
  "peak_tilt_rad": 0.05712055231767432,
  "peak_wheel_torque_nm": 0.5938960313796997,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 23.434337929997128
}
```
