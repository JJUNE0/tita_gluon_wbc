# tita_flash_sac_115632_883848_model_5000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "1903dc0286854480cbd71a78d99118cf34b42a59fcbc2c095c72fc6cc464179e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0150025031379668,
  "max_drift_m": 0.031884737860048765,
  "radial_IAE_m_s": 0.7898908140912162,
  "signed_longitudinal_delta_m": -0.014998446431540436,
  "tail_speed_mean_m_s": -0.00010354315784779062,
  "tail_speed_rms_m_s": 0.001070448453788557,
  "tail_sensor_speed_mean_m_s": -6.957755194717973e-05,
  "tail_fk_speed_mean_m_s": -7.802951942286855e-05,
  "peak_tilt_rad": 0.1617057409260052,
  "peak_wheel_torque_nm": 2.978593349456787,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2239433649749932,
  "final_integral_m_s": -0.2239433649749932,
  "elapsed_wall_s": 12.045771792996675
}
```
