# tita_flash_sac_115632_883848_model_60000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
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
  "initial_physics_sha256": "4c4ffc8869defe63b47a3f1b603e41d9094be3ae9662d07da1ba76b168ba4ab8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0027135274499140794,
  "max_drift_m": 0.007958595333825381,
  "radial_IAE_m_s": 0.18215609485488474,
  "signed_longitudinal_delta_m": 0.002690603839448221,
  "tail_speed_mean_m_s": -2.4896336224750488e-05,
  "tail_speed_rms_m_s": 2.564647263525398e-05,
  "tail_sensor_speed_mean_m_s": -2.4913475017292384e-05,
  "tail_fk_speed_mean_m_s": -2.2808392813472558e-05,
  "peak_tilt_rad": 0.06929002880083357,
  "peak_wheel_torque_nm": 0.19094218313694,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.047458168851638866,
  "final_integral_m_s": 0.047458168851638866,
  "elapsed_wall_s": 13.464035256009083
}
```
