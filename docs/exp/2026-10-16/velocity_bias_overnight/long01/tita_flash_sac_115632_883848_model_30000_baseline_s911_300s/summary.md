# tita_flash_sac_115632_883848_model_30000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "26a376cc47577621dc20f38a072a5e748c62c4fbf1e1240362aa022dafb41670",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 66.52979931007907,
  "max_drift_m": 66.52979931007907,
  "radial_IAE_m_s": 10232.23202673694,
  "signed_longitudinal_delta_m": 59.676583272437064,
  "tail_speed_mean_m_s": 0.23089981401474896,
  "tail_speed_rms_m_s": 0.23089981402441387,
  "tail_sensor_speed_mean_m_s": 0.23039987642501594,
  "tail_fk_speed_mean_m_s": 0.23039801663827025,
  "peak_tilt_rad": 0.12696275551672853,
  "peak_wheel_torque_nm": 0.14372336864471436,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 39.90428557898849
}
```
