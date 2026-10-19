# tita_flash_sac_193248_068255_model_50000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "8edfb571b0d164d79960c0bf8a36a9d64532f44b05fe15b75be2ec363b283dc6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.957787049139209,
  "max_drift_m": 6.957787049139209,
  "radial_IAE_m_s": 198.35518302724023,
  "signed_longitudinal_delta_m": 6.955287071706577,
  "tail_speed_mean_m_s": 0.12546757162869077,
  "tail_speed_rms_m_s": 0.12547320916578894,
  "tail_sensor_speed_mean_m_s": 0.12519643752744555,
  "tail_fk_speed_mean_m_s": 0.12519479683316043,
  "peak_tilt_rad": 0.05837113361298796,
  "peak_wheel_torque_nm": 0.2605375349521637,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.023407116997987
}
```
