# tita_flash_sac_115632_883848_model_5000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
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
  "initial_physics_sha256": "65218c0f51ba1e8e455ead804618fb3569f6936691847505c6cd07e05f04b918",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.017626142549637475,
  "max_drift_m": 0.09632266913955712,
  "radial_IAE_m_s": 4.187206294346423,
  "signed_longitudinal_delta_m": 0.017539329973152256,
  "tail_speed_mean_m_s": -1.4006440832945844e-05,
  "tail_speed_rms_m_s": 0.0002549103781561575,
  "tail_sensor_speed_mean_m_s": 8.78852951889576e-06,
  "tail_fk_speed_mean_m_s": 9.283398326149661e-08,
  "peak_tilt_rad": 0.19672923138120235,
  "peak_wheel_torque_nm": 3.3272833824157715,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4095377942627315,
  "final_integral_m_s": -0.4095377942627315,
  "elapsed_wall_s": 76.47978694998892
}
```
