# tita_flash_sac_115632_883848_model_60000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "d6047cc60b8fe8566eb957577e66d638462fc65a0854f0076b6575b22aeeacb3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004454411513205032,
  "max_drift_m": 0.007034627851363285,
  "radial_IAE_m_s": 0.2761386066282597,
  "signed_longitudinal_delta_m": 0.004439140709878716,
  "tail_speed_mean_m_s": -1.1222204313491822e-05,
  "tail_speed_rms_m_s": 1.147870753628542e-05,
  "tail_sensor_speed_mean_m_s": -1.1268524477598817e-05,
  "tail_fk_speed_mean_m_s": -9.16426579463495e-06,
  "peak_tilt_rad": 0.0692899820872479,
  "peak_wheel_torque_nm": 0.20092031359672546,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04742844848956608,
  "final_integral_m_s": 0.04744077053028991,
  "elapsed_wall_s": 5.960288998030592
}
```
