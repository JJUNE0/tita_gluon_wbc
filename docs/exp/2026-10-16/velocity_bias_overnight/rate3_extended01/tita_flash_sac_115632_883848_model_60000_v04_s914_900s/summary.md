# tita_flash_sac_115632_883848_model_60000_v04_s914_900s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_v04_s914_900s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
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
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "1ff916b458aff131929055d6e4a56ccf621e06306bd67b1df2ef032e8abb86c3",
  "complete": true,
  "failure": [],
  "duration_s": 900.0,
  "final_drift_m": 0.006405636644080074,
  "max_drift_m": 0.007942557993084624,
  "radial_IAE_m_s": 3.245890544224722,
  "signed_longitudinal_delta_m": -0.0005036745451869864,
  "tail_speed_mean_m_s": -1.1466476270332346e-05,
  "tail_speed_rms_m_s": 1.1466611574772277e-05,
  "tail_sensor_speed_mean_m_s": -1.2799852500619307e-05,
  "tail_fk_speed_mean_m_s": -2.6377554676994177e-08,
  "peak_tilt_rad": 0.06924176109374236,
  "peak_wheel_torque_nm": 0.19151586294174194,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.044688647634181206,
  "final_integral_m_s": 0.044688647634181206,
  "elapsed_wall_s": 155.3576041579945
}
```
