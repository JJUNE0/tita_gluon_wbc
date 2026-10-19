# tita_flash_sac_115632_883848_model_60000_friction08_v04_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction08_v04_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "d833d3943fe48908650e8d22fc3ac3333311a5d1d7cc2d6dbbce7ff94bd15443"
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
  "initial_physics_sha256": "9064ed9941d862540cf642fcf2dbf29af5780286ee8c63e78bd4563550e065da",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.0035305401533352434,
  "max_drift_m": 0.00801811815937626,
  "radial_IAE_m_s": 0.9660678620472115,
  "signed_longitudinal_delta_m": 0.003373009846697435,
  "tail_speed_mean_m_s": -5.778437313829114e-06,
  "tail_speed_rms_m_s": 8.487136488106248e-06,
  "tail_sensor_speed_mean_m_s": -6.412952823977621e-06,
  "tail_fk_speed_mean_m_s": -4.322302554907228e-06,
  "peak_tilt_rad": 0.0701125392875761,
  "peak_wheel_torque_nm": 0.1901119351387024,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.052635471307733106,
  "final_integral_m_s": 0.052635471307733106,
  "elapsed_wall_s": 29.472566969052423
}
```
