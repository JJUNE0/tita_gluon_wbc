# tita_flash_sac_115632_883848_model_60000_mass13_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass13_v01_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "initial_physics_sha256": "5778aa7084ae1a9bdba6b9dda016e1318e27c07ad5f84a80c847cf7b0979bf35",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.040534074013160795,
  "max_drift_m": 0.06236590870283818,
  "radial_IAE_m_s": 2.4005325636192776,
  "signed_longitudinal_delta_m": -0.04051096301561521,
  "tail_speed_mean_m_s": 8.118196625075919e-06,
  "tail_speed_rms_m_s": 0.01783686834938198,
  "tail_sensor_speed_mean_m_s": 0.0011217005316771305,
  "tail_fk_speed_mean_m_s": 3.3070501477913896e-05,
  "peak_tilt_rad": 0.17384484889743823,
  "peak_wheel_torque_nm": 6.017722129821777,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3736863806468289,
  "final_integral_m_s": -0.40439637845308796,
  "elapsed_wall_s": 4.925764519022778
}
```
