# tita_flash_sac_115632_883848_model_60000_com-0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com-0.005_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "6e852968a0a45508ece30abc12e1254f266760f5b7fa9c9871bc3a2c572e626f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.000659793529753306,
  "max_drift_m": 0.000659793529753306,
  "radial_IAE_m_s": 0.0266039825758482,
  "signed_longitudinal_delta_m": 0.00014324026114016043,
  "tail_speed_mean_m_s": 1.300907098381483e-05,
  "tail_speed_rms_m_s": 1.3345371243033593e-05,
  "tail_sensor_speed_mean_m_s": 1.2839115197826644e-05,
  "tail_fk_speed_mean_m_s": 1.5175507378080601e-05,
  "peak_tilt_rad": 0.066932299356119,
  "peak_wheel_torque_nm": 0.11942539364099503,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0032111087975923605,
  "final_integral_m_s": 0.0031769778001470945,
  "elapsed_wall_s": 5.379027733986732
}
```
