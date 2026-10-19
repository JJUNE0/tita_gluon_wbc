# tita_flash_sac_193248_068255_model_95000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
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
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "a69492bdb4f4a37bc2982ad18fdf4cca85ab984657c0e32367b5b85236a2ece6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022449292602240604,
  "max_drift_m": 0.05230737847346507,
  "radial_IAE_m_s": 1.3530577033360567,
  "signed_longitudinal_delta_m": -0.022443164623644544,
  "tail_speed_mean_m_s": 7.641980251145476e-07,
  "tail_speed_rms_m_s": 7.653299054549551e-07,
  "tail_sensor_speed_mean_m_s": 1.030592395250223e-06,
  "tail_fk_speed_mean_m_s": 4.005842945428874e-07,
  "peak_tilt_rad": 0.08062007155788975,
  "peak_wheel_torque_nm": 0.5261504650115967,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2371598168263,
  "final_integral_m_s": -0.2371605584916255,
  "elapsed_wall_s": 14.020269838976674
}
```
