# tita_flash_sac_193248_068255_model_20000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
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
  "initial_physics_sha256": "4891bf645a774fa1dd23b6b263393877a393381596f4eb091be10c058156a8f2",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.057641393393610275,
  "max_drift_m": 0.08909146972783112,
  "radial_IAE_m_s": 18.26408402605773,
  "signed_longitudinal_delta_m": 0.05724335130499822,
  "tail_speed_mean_m_s": -4.202507514948754e-05,
  "tail_speed_rms_m_s": 4.2072443622885686e-05,
  "tail_sensor_speed_mean_m_s": -2.7235999444926365e-05,
  "tail_fk_speed_mean_m_s": -1.363644622096303e-05,
  "peak_tilt_rad": 0.15130798638179943,
  "peak_wheel_torque_nm": 1.6480180025100708,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6519034614652105,
  "final_integral_m_s": 0.6519427350631691,
  "elapsed_wall_s": 57.61177569098072
}
```
