# tita_flash_sac_115632_883848_model_5000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
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
  "initial_physics_sha256": "1c7466b0931c77cfeb9376742c740605948a92ff2ff2563b03a480164769bbd6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007156626149660582,
  "max_drift_m": 0.13091526493729747,
  "radial_IAE_m_s": 0.7546345388317787,
  "signed_longitudinal_delta_m": 0.007076721638860644,
  "tail_speed_mean_m_s": -2.283084549220295e-05,
  "tail_speed_rms_m_s": 0.0014897453960122508,
  "tail_sensor_speed_mean_m_s": -2.557758677288622e-05,
  "tail_fk_speed_mean_m_s": -1.0245924418144447e-05,
  "peak_tilt_rad": 0.19914443212085553,
  "peak_wheel_torque_nm": 5.402998924255371,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4521733204558058,
  "final_integral_m_s": -0.4521733204558058,
  "elapsed_wall_s": 10.290987156971823
}
```
