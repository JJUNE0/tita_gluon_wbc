# tita_flash_sac_115632_883848_model_5000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
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
  "initial_physics_sha256": "f1d9b38c5c736f172e1bbcfe6378fd92c7f9ffd462daba7b62d38642205a011a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006859650993404796,
  "max_drift_m": 0.10145586474454066,
  "radial_IAE_m_s": 0.7721593861084296,
  "signed_longitudinal_delta_m": 0.006779084629339479,
  "tail_speed_mean_m_s": -6.096996653925558e-06,
  "tail_speed_rms_m_s": 0.0015810717293882508,
  "tail_sensor_speed_mean_m_s": -6.034914753570801e-06,
  "tail_fk_speed_mean_m_s": 4.338113200646175e-06,
  "peak_tilt_rad": 0.19786934028699088,
  "peak_wheel_torque_nm": 3.2878050804138184,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.44589523870206965,
  "final_integral_m_s": -0.44589523870206965,
  "elapsed_wall_s": 10.385359827021603
}
```
