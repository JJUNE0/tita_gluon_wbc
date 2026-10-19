# tita_flash_sac_115632_883848_model_60000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "2cd71d990e166e840d89c0bd86ae595b10fa88dbadb2ca640f4bb2147e855f2a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0012919721599759881,
  "max_drift_m": 0.016070898232098212,
  "radial_IAE_m_s": 0.06356696119475813,
  "signed_longitudinal_delta_m": -0.0012862527004245362,
  "tail_speed_mean_m_s": -2.265493281932782e-05,
  "tail_speed_rms_m_s": 2.4326304920058994e-05,
  "tail_sensor_speed_mean_m_s": -2.243808307786592e-05,
  "tail_fk_speed_mean_m_s": -2.0649589049915228e-05,
  "peak_tilt_rad": 0.07289111096276724,
  "peak_wheel_torque_nm": 0.30323854088783264,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08984125400473957,
  "final_integral_m_s": 0.08984125400473957,
  "elapsed_wall_s": 10.814871876034886
}
```
