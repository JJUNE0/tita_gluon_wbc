# tita_flash_sac_115632_883848_model_60000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "5315c098dcd443d4a8a510dca0c01095167d1a6b45c0eaab75c14ce8c3d1712e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0013748205026622576,
  "max_drift_m": 0.08245288847126223,
  "radial_IAE_m_s": 0.23684253720906934,
  "signed_longitudinal_delta_m": 0.0012692925697960482,
  "tail_speed_mean_m_s": -2.529650388114343e-05,
  "tail_speed_rms_m_s": 2.5861615912275407e-05,
  "tail_sensor_speed_mean_m_s": -2.533492170923009e-05,
  "tail_fk_speed_mean_m_s": -2.3198696210696116e-05,
  "peak_tilt_rad": 0.09500622067220377,
  "peak_wheel_torque_nm": 1.5645419359207153,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.047390332927911234,
  "final_integral_m_s": 0.047390332927911234,
  "elapsed_wall_s": 8.987494460016023
}
```
