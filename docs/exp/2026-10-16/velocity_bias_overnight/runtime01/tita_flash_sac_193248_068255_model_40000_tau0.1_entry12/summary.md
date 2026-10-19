# tita_flash_sac_193248_068255_model_40000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "12486bbd1f825f003d4a6cf51aaf62087d27b089ada15a38f892eaced670541e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024472131908705886,
  "max_drift_m": 0.0437357743835317,
  "radial_IAE_m_s": 1.4183673458217139,
  "signed_longitudinal_delta_m": 0.02447211260117999,
  "tail_speed_mean_m_s": 3.05206937795292e-05,
  "tail_speed_rms_m_s": 3.0533437516480484e-05,
  "tail_sensor_speed_mean_m_s": 3.083325960599473e-05,
  "tail_fk_speed_mean_m_s": 3.0190354409413814e-05,
  "peak_tilt_rad": 0.10845431933704552,
  "peak_wheel_torque_nm": 0.8908416032791138,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2579098212657998,
  "final_integral_m_s": 0.2578474108909928,
  "elapsed_wall_s": 5.915197398979217
}
```
