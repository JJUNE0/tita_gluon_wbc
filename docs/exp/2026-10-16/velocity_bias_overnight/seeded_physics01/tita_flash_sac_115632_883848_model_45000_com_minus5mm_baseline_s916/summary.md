# tita_flash_sac_115632_883848_model_45000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "f2596270544d4dcf2913fcf9729b96b992f0ed96f2708cc1349540ce3841ee59",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.239158476451339,
  "max_drift_m": 2.239158476451339,
  "radial_IAE_m_s": 65.635657675632,
  "signed_longitudinal_delta_m": 2.1673952634657025,
  "tail_speed_mean_m_s": 0.03890260305735813,
  "tail_speed_rms_m_s": 0.03948989444076949,
  "tail_sensor_speed_mean_m_s": 0.03859981294469437,
  "tail_fk_speed_mean_m_s": 0.03890516617131368,
  "peak_tilt_rad": 0.05171857688553594,
  "peak_wheel_torque_nm": 2.781035900115967,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.51163775200257
}
```
