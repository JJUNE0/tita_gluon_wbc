# tita_flash_sac_193248_068255_model_40000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "final_drift_m": 0.02446492384539682,
  "max_drift_m": 0.04174903272476672,
  "radial_IAE_m_s": 1.4180134248510399,
  "signed_longitudinal_delta_m": 0.02446490184558228,
  "tail_speed_mean_m_s": 3.051336048268217e-05,
  "tail_speed_rms_m_s": 3.052565969871885e-05,
  "tail_sensor_speed_mean_m_s": 3.082584281350872e-05,
  "tail_fk_speed_mean_m_s": 3.0183237352377026e-05,
  "peak_tilt_rad": 0.10838830872821514,
  "peak_wheel_torque_nm": 0.9815006256103516,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2578857068548782,
  "final_integral_m_s": 0.2578232186486053,
  "elapsed_wall_s": 5.945291186042596
}
```
