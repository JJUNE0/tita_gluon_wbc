# tita_flash_sac_115632_883848_model_30000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "c797f040ada22126b9af4adc7f42b49786de8bec503bc7fab90d4a0db1ac8986",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021174686508889172,
  "max_drift_m": 0.11355513420966828,
  "radial_IAE_m_s": 1.358435540967926,
  "signed_longitudinal_delta_m": -0.021159400077895307,
  "tail_speed_mean_m_s": -7.201197562388608e-05,
  "tail_speed_rms_m_s": 8.346897018000387e-05,
  "tail_sensor_speed_mean_m_s": -7.292542111214281e-05,
  "tail_fk_speed_mean_m_s": -7.146260498583992e-05,
  "peak_tilt_rad": 0.1263082952532686,
  "peak_wheel_torque_nm": 0.7936463952064514,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.55874980722998,
  "final_integral_m_s": 0.55874980722998,
  "elapsed_wall_s": 16.042147070984356
}
```
