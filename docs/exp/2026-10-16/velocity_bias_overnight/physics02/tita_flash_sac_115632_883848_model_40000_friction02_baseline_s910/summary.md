# tita_flash_sac_115632_883848_model_40000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "642ebc5b304ecc03661297ec2228d6e312b4187624a45dc961d516ea881eb927",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.090301853609585,
  "max_drift_m": 6.090301853609585,
  "radial_IAE_m_s": 191.74926140791575,
  "signed_longitudinal_delta_m": 4.4141710887681,
  "tail_speed_mean_m_s": 0.11206435368942476,
  "tail_speed_rms_m_s": 0.1120643537124005,
  "tail_sensor_speed_mean_m_s": 0.11199234725633818,
  "tail_fk_speed_mean_m_s": 0.11200935478628112,
  "peak_tilt_rad": 0.108545163310382,
  "peak_wheel_torque_nm": 0.21976059675216675,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.495656427985523
}
```
