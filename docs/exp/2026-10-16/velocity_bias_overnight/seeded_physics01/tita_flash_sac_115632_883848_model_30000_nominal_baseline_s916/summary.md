# tita_flash_sac_115632_883848_model_30000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "3af109cd27a81ab6eba23510e9cbd221e44b73f1ef3eb55e316fb413e0381503",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.060747916287324,
  "max_drift_m": 14.060747916287324,
  "radial_IAE_m_s": 426.0300398405527,
  "signed_longitudinal_delta_m": 14.04300687905129,
  "tail_speed_mean_m_s": 0.23132622955616033,
  "tail_speed_rms_m_s": 0.23132631555296299,
  "tail_sensor_speed_mean_m_s": 0.23082514870959073,
  "tail_fk_speed_mean_m_s": 0.23082355525804202,
  "peak_tilt_rad": 0.12712721730558885,
  "peak_wheel_torque_nm": 0.1439915895462036,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.701311009004712
}
```
