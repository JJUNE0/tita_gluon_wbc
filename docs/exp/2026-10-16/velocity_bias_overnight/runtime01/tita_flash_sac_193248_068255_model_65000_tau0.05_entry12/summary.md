# tita_flash_sac_193248_068255_model_65000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "ff698c5607c2c0c8604f83883d6d683ea9b28df2ecf598137df012cf6d0dba46",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.018359331188236246,
  "max_drift_m": 0.027030058067667156,
  "radial_IAE_m_s": 1.129047632227702,
  "signed_longitudinal_delta_m": -0.018351836018180034,
  "tail_speed_mean_m_s": 1.3144547448720437e-05,
  "tail_speed_rms_m_s": 1.314629163082517e-05,
  "tail_sensor_speed_mean_m_s": 1.2660238591839091e-05,
  "tail_fk_speed_mean_m_s": 1.407583837776167e-05,
  "peak_tilt_rad": 0.048863949589374345,
  "peak_wheel_torque_nm": 0.2775365710258484,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18790493591559115,
  "final_integral_m_s": -0.18793239044724358,
  "elapsed_wall_s": 15.47257699497277
}
```
