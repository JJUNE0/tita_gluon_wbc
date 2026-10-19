# tita_flash_sac_115632_883848_model_5000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "be6de9cb201f1263cf5e7c3ab806b4d593f99d65fe40d5664e87ec98c0825691",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00897624598848297,
  "max_drift_m": 0.09632248660004882,
  "radial_IAE_m_s": 0.8547622371937731,
  "signed_longitudinal_delta_m": 0.008898607762139752,
  "tail_speed_mean_m_s": 7.295838519947311e-05,
  "tail_speed_rms_m_s": 0.001813607843799348,
  "tail_sensor_speed_mean_m_s": 7.916501927046743e-05,
  "tail_fk_speed_mean_m_s": 8.541754872968287e-05,
  "peak_tilt_rad": 0.19672920904136681,
  "peak_wheel_torque_nm": 3.327282667160034,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.44970325820078605,
  "final_integral_m_s": -0.44970325820078605,
  "elapsed_wall_s": 10.192480546014849
}
```
