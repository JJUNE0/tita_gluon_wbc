# tita_flash_sac_115632_883848_model_60000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "7d7491eeb6b4937c1919ea4e21113b024dad55c0f9683f167fb025b6003e0b93",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03895458163519709,
  "max_drift_m": 0.06412283535181937,
  "radial_IAE_m_s": 2.4030944601820865,
  "signed_longitudinal_delta_m": -0.038947874820514,
  "tail_speed_mean_m_s": 5.741465958106746e-05,
  "tail_speed_rms_m_s": 0.016550105747477062,
  "tail_sensor_speed_mean_m_s": -0.0014200146049525076,
  "tail_fk_speed_mean_m_s": -7.341757931739831e-05,
  "peak_tilt_rad": 0.17471128137464276,
  "peak_wheel_torque_nm": 5.478490352630615,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.42373803588115144,
  "final_integral_m_s": -0.42150051366585006,
  "elapsed_wall_s": 17.93882175098406
}
```
