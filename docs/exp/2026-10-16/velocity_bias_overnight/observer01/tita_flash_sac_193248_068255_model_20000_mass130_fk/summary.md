# tita_flash_sac_193248_068255_model_20000_mass130_fk

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_mass130_fk",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
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
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "9423649c8cc479e764bacc4e978dcae6fd0bd620413676a2e35f8f30cfef4b0b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009189873955710486,
  "max_drift_m": 0.016902000073068912,
  "radial_IAE_m_s": 0.5514368078327248,
  "signed_longitudinal_delta_m": -0.009188405737034314,
  "tail_speed_mean_m_s": -9.341741483864475e-07,
  "tail_speed_rms_m_s": 9.374157819156763e-07,
  "tail_sensor_speed_mean_m_s": -4.513904441296265e-07,
  "tail_fk_speed_mean_m_s": 2.5009154347702997e-10,
  "peak_tilt_rad": 0.18657359255626105,
  "peak_wheel_torque_nm": 0.7599528431892395,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.09729489933485641,
  "final_integral_m_s": -0.097294994359065,
  "elapsed_wall_s": 13.479856150050182
}
```
