# tita_flash_sac_193248_068255_model_65000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "d1ffb587b3e1db2827ff5262655c37108fe4d9ec91e3d0a7bae949eb0d406f71",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.828787417845808,
  "max_drift_m": 2.828787417845808,
  "radial_IAE_m_s": 91.56745056738286,
  "signed_longitudinal_delta_m": -2.825976205544339,
  "tail_speed_mean_m_s": -0.0429243757562186,
  "tail_speed_rms_m_s": 0.042924812039130164,
  "tail_sensor_speed_mean_m_s": -0.04283809571664537,
  "tail_fk_speed_mean_m_s": -0.04283293162174357,
  "peak_tilt_rad": 0.029440521773254735,
  "peak_wheel_torque_nm": 1.7681365013122559,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.3618283290416
}
```
