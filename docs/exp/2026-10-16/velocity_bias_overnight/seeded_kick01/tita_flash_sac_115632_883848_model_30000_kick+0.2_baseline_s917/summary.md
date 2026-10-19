# tita_flash_sac_115632_883848_model_30000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "7bf6e40827d9c995a409d450ca2c26e3b7a0995664ac88cee049da12f22fb704",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.164141347037955,
  "max_drift_m": 14.164141347037955,
  "radial_IAE_m_s": 432.32161073189155,
  "signed_longitudinal_delta_m": 14.143031549048706,
  "tail_speed_mean_m_s": 0.231307889049364,
  "tail_speed_rms_m_s": 0.23130796760267017,
  "tail_sensor_speed_mean_m_s": 0.23080686158305977,
  "tail_fk_speed_mean_m_s": 0.2308052523812387,
  "peak_tilt_rad": 0.14630644551449223,
  "peak_wheel_torque_nm": 2.0345242023468018,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.990412148996256
}
```
