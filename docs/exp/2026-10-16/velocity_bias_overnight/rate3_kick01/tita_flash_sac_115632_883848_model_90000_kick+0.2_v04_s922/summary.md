# tita_flash_sac_115632_883848_model_90000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "bc5ac01e5d84fc2106e771481df32bcd28ad357efbd9f8501e4fab2bf3fb6cfc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04635631287359683,
  "max_drift_m": 0.14915996775089665,
  "radial_IAE_m_s": 2.774851436476463,
  "signed_longitudinal_delta_m": 0.046356009393916875,
  "tail_speed_mean_m_s": 9.245565066233093e-05,
  "tail_speed_rms_m_s": 9.404774826669859e-05,
  "tail_sensor_speed_mean_m_s": 9.1978805471199e-05,
  "tail_fk_speed_mean_m_s": 9.31351345618963e-05,
  "peak_tilt_rad": 0.08428429177467711,
  "peak_wheel_torque_nm": 1.8617579936981201,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3909649705914852,
  "final_integral_m_s": 0.3909649705914852,
  "elapsed_wall_s": 8.011289646034129
}
```
