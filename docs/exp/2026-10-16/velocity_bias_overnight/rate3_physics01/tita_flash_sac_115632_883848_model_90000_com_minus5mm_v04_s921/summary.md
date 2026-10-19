# tita_flash_sac_115632_883848_model_90000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "d481b14d32c38070e8fc52f948d8ca9f674cf77a75c0a95e93bf35c4759d989f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.046348353036251566,
  "max_drift_m": 0.05396531608470784,
  "radial_IAE_m_s": 2.6460616131268764,
  "signed_longitudinal_delta_m": 0.046346121119783354,
  "tail_speed_mean_m_s": 7.377191553859023e-05,
  "tail_speed_rms_m_s": 7.640904861964198e-05,
  "tail_sensor_speed_mean_m_s": 7.331615951293728e-05,
  "tail_fk_speed_mean_m_s": 7.450419535888436e-05,
  "peak_tilt_rad": 0.06778929038860504,
  "peak_wheel_torque_nm": 0.27181458473205566,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.33755867068857937,
  "final_integral_m_s": 0.33755867068857937,
  "elapsed_wall_s": 13.184256293985527
}
```
