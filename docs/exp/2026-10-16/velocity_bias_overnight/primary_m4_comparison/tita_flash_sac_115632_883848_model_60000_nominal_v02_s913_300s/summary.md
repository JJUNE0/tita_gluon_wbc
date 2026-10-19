# tita_flash_sac_115632_883848_model_60000_nominal_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_nominal_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "767b3e7f7847a8e838f15e263b866e6ed7630cea5577e18891611065effc766c",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.00447016256346121,
  "max_drift_m": 0.007058658873391176,
  "radial_IAE_m_s": 1.3646145898002795,
  "signed_longitudinal_delta_m": 0.004367203964204005,
  "tail_speed_mean_m_s": -7.4719077250124e-07,
  "tail_speed_rms_m_s": 7.690538005381046e-07,
  "tail_sensor_speed_mean_m_s": -1.557176740567317e-06,
  "tail_fk_speed_mean_m_s": 5.954797070336521e-07,
  "peak_tilt_rad": 0.06939400622474179,
  "peak_wheel_torque_nm": 0.20095942914485931,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.05270934584750623,
  "final_integral_m_s": 0.0527080011974883,
  "elapsed_wall_s": 78.54098952002823
}
```
