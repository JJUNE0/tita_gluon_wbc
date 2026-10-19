# tita_flash_sac_115632_883848_model_45000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "6f721d9f26204e40c5eb90545361dc8d9d2be1251ed98d0817c17de83733e34a",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.018358995327687876,
  "max_drift_m": 0.033631049815146176,
  "radial_IAE_m_s": 3.5093151443630166,
  "signed_longitudinal_delta_m": 0.006898313086278336,
  "tail_speed_mean_m_s": -0.00038588144643800486,
  "tail_speed_rms_m_s": 0.011324332678785218,
  "tail_sensor_speed_mean_m_s": -0.002458585779667836,
  "tail_fk_speed_mean_m_s": 3.439576127640067e-05,
  "peak_tilt_rad": 0.04861898658224795,
  "peak_wheel_torque_nm": 4.630244731903076,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03585521522374214,
  "final_integral_m_s": -0.03585521522374214,
  "elapsed_wall_s": 51.73237847699784
}
```
