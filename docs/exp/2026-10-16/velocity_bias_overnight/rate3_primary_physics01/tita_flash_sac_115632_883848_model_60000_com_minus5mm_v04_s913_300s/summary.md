# tita_flash_sac_115632_883848_model_60000_com_minus5mm_v04_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com_minus5mm_v04_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "fe0ce59e2ecfc91c47bba60dcfeecec831868c751be20b59d55275193d9057cf",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.008827590567526565,
  "max_drift_m": 0.008836720314960649,
  "radial_IAE_m_s": 2.028689686650048,
  "signed_longitudinal_delta_m": 0.008322726685024378,
  "tail_speed_mean_m_s": 2.067786729439047e-06,
  "tail_speed_rms_m_s": 3.769749900046371e-06,
  "tail_sensor_speed_mean_m_s": 1.2668496807396674e-06,
  "tail_fk_speed_mean_m_s": 3.5880721543709987e-06,
  "peak_tilt_rad": 0.06912828446264419,
  "peak_wheel_torque_nm": 0.16114439070224762,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.017750050955583845,
  "final_integral_m_s": 0.017750050955583845,
  "elapsed_wall_s": 29.51852990797488
}
```
