# tita_flash_sac_193248_068255_model_40000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "final_drift_m": 0.024490286538446423,
  "max_drift_m": 0.04896746797244263,
  "radial_IAE_m_s": 1.420863603049506,
  "signed_longitudinal_delta_m": 0.024490273401999392,
  "tail_speed_mean_m_s": 3.0531223087815124e-05,
  "tail_speed_rms_m_s": 3.0545136321740246e-05,
  "tail_sensor_speed_mean_m_s": 3.084287185275922e-05,
  "tail_fk_speed_mean_m_s": 3.020114530399171e-05,
  "peak_tilt_rad": 0.10852681438587086,
  "peak_wheel_torque_nm": 0.6739453077316284,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2579734339466517,
  "final_integral_m_s": 0.25791107088879395,
  "elapsed_wall_s": 5.988744353002403
}
```
