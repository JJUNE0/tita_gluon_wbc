# p009_tita_flash_sac_115632_883848_model_5000_kick+0.0

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p009_tita_flash_sac_115632_883848_model_5000_kick+0.0",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.5,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 1.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "750b8cb4997d587a4f1491c373224fee70bf03a6a0994bf1f9ecdd82a7620ccf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009894992205942203,
  "max_drift_m": 0.1219725810449183,
  "radial_IAE_m_s": 0.8671817110068706,
  "signed_longitudinal_delta_m": 0.009856865759111093,
  "tail_speed_mean_m_s": 7.780158706298733e-05,
  "tail_speed_rms_m_s": 0.0002101645384722419,
  "tail_sensor_speed_mean_m_s": 8.768077325774656e-05,
  "tail_fk_speed_mean_m_s": 9.129831279822704e-05,
  "peak_tilt_rad": 0.1975127777715422,
  "peak_wheel_torque_nm": 3.6346826553344727,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.45134265700307685,
  "final_integral_m_s": -0.45134265700307685,
  "elapsed_wall_s": 8.972684342996217
}
```
