# tita_flash_sac_115632_883848_model_30000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "a6bf79a1c6ed7634a39280dcc5a50c0ccb73b57d376417e8117fab1a5f929b83",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.159416931186607,
  "max_drift_m": 14.159416931186607,
  "radial_IAE_m_s": 432.1027985934096,
  "signed_longitudinal_delta_m": 14.136376126736442,
  "tail_speed_mean_m_s": 0.23129963466352568,
  "tail_speed_rms_m_s": 0.23129971005890312,
  "tail_sensor_speed_mean_m_s": 0.23079862965140277,
  "tail_fk_speed_mean_m_s": 0.23079701435483355,
  "peak_tilt_rad": 0.14618884194433068,
  "peak_wheel_torque_nm": 2.036938428878784,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.900145415973384
}
```
