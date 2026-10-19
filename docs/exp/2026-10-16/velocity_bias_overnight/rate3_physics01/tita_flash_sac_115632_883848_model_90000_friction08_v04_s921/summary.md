# tita_flash_sac_115632_883848_model_90000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "initial_physics_sha256": "e82c51a8c0d0b9ed1f32311a4570491d16ee5fbf1c2ce02c6aaeb3eb1d5eec5a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04398265128603945,
  "max_drift_m": 0.05935578455714634,
  "radial_IAE_m_s": 2.4702040523925155,
  "signed_longitudinal_delta_m": 0.043981344943295586,
  "tail_speed_mean_m_s": 0.00011745739783321182,
  "tail_speed_rms_m_s": 0.00012308495719942576,
  "tail_sensor_speed_mean_m_s": 0.00011678451861490524,
  "tail_fk_speed_mean_m_s": 0.000118104088028863,
  "peak_tilt_rad": 0.0701171004339518,
  "peak_wheel_torque_nm": 0.3961781859397888,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3844699175771363,
  "final_integral_m_s": 0.3844699175771363,
  "elapsed_wall_s": 14.431264952989295
}
```
