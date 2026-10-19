# tita_flash_sac_115632_883848_model_85000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "139371344e21f51f2e471a0fc9999166635043836b7cf30e2b49c17f3385c4df",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.373309789437403,
  "max_drift_m": 8.373309789437403,
  "radial_IAE_m_s": 255.27470765134683,
  "signed_longitudinal_delta_m": 8.26699496170868,
  "tail_speed_mean_m_s": 0.13542480271858837,
  "tail_speed_rms_m_s": 0.1354259714538908,
  "tail_sensor_speed_mean_m_s": 0.13513447235058015,
  "tail_fk_speed_mean_m_s": 0.13513507856581689,
  "peak_tilt_rad": 0.06917313826954019,
  "peak_wheel_torque_nm": 0.20363080501556396,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.431337247951888
}
```
