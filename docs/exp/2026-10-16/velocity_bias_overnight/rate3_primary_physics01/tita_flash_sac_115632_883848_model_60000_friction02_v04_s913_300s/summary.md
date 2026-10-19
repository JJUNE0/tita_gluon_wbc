# tita_flash_sac_115632_883848_model_60000_friction02_v04_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction02_v04_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "320c1433872100d9a89952b28db46fac857c641a1c6d24bb8d6278d2ddeb2762",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.003990585412396849,
  "max_drift_m": 0.007684840604070565,
  "radial_IAE_m_s": 1.2854257496907806,
  "signed_longitudinal_delta_m": -0.003965230138704342,
  "tail_speed_mean_m_s": 8.043477518855973e-07,
  "tail_speed_rms_m_s": 8.145719216191477e-07,
  "tail_sensor_speed_mean_m_s": -3.453077520094211e-05,
  "tail_fk_speed_mean_m_s": 7.145805143456311e-08,
  "peak_tilt_rad": 0.06149666934956999,
  "peak_wheel_torque_nm": 0.1778925657272339,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04235407779151711,
  "final_integral_m_s": 0.04235407779151711,
  "elapsed_wall_s": 29.88238426600583
}
```
