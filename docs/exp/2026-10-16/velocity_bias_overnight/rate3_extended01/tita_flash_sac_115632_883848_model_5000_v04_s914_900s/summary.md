# tita_flash_sac_115632_883848_model_5000_v04_s914_900s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_v04_s914_900s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 900.0,
    "warmup": 1.2,
    "seed": 914,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "e67b65d9dd572b37c5fc984eba9110379400d67230f825ed965cb5fca0f159f4",
  "complete": true,
  "failure": [],
  "duration_s": 900.0,
  "final_drift_m": 0.023287818074649153,
  "max_drift_m": 0.09550591176695256,
  "radial_IAE_m_s": 17.50670200539595,
  "signed_longitudinal_delta_m": 0.02321638447505804,
  "tail_speed_mean_m_s": -4.886466948348712e-06,
  "tail_speed_rms_m_s": 4.887120925674013e-06,
  "tail_sensor_speed_mean_m_s": 7.043815120602614e-06,
  "tail_fk_speed_mean_m_s": 4.840091305038687e-09,
  "peak_tilt_rad": 0.19649338998272126,
  "peak_wheel_torque_nm": 3.325157403945923,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3949797607969885,
  "final_integral_m_s": -0.3949797607969885,
  "elapsed_wall_s": 189.32560731703416
}
```
