# tita_flash_sac_115632_883848_model_60000_mass115_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass115_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "de102d7b611657224b65a0cfa5b6c6a8b03b2ba0da773d30b4afd17f4b348517",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.024524544387362828,
  "max_drift_m": 0.035018090504613075,
  "radial_IAE_m_s": 6.854508547890722,
  "signed_longitudinal_delta_m": -0.02452452672039409,
  "tail_speed_mean_m_s": 1.721506984459111e-06,
  "tail_speed_rms_m_s": 1.7260241805839412e-06,
  "tail_sensor_speed_mean_m_s": 1.2699491827151514e-06,
  "tail_fk_speed_mean_m_s": 2.367291877757348e-06,
  "peak_tilt_rad": 0.1133038816289631,
  "peak_wheel_torque_nm": 0.6414422392845154,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.25198101379165083,
  "final_integral_m_s": -0.2519859351758225,
  "elapsed_wall_s": 64.29640597500838
}
```
