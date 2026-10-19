# tita_flash_sac_115632_883848_model_75000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
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
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "f6c5b80d2f599ac01863d1b5649b58d51c3e3522d95a198a64b245315e14ccc2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.038545103270571056,
  "max_drift_m": 0.05013092544260479,
  "radial_IAE_m_s": 2.229140077826891,
  "signed_longitudinal_delta_m": 0.0385416456311635,
  "tail_speed_mean_m_s": 2.4665605696890154e-05,
  "tail_speed_rms_m_s": 2.4910249982159176e-05,
  "tail_sensor_speed_mean_m_s": 2.4673563236808537e-05,
  "tail_fk_speed_mean_m_s": 2.5327164755939357e-05,
  "peak_tilt_rad": 0.06720187989315396,
  "peak_wheel_torque_nm": 0.36030077934265137,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.004832558365400923,
  "final_integral_m_s": 0.004832558365400923,
  "elapsed_wall_s": 12.451404211984482
}
```
