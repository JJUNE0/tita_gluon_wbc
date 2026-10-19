# tita_flash_sac_115632_883848_model_100000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "626296b4ffb97098a43630e215acaed163e20e00083f6a26407ba03114d18331",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.093006873559415,
  "max_drift_m": 0.11352193977243023,
  "radial_IAE_m_s": 28.181179705928468,
  "signed_longitudinal_delta_m": 0.09300442750950526,
  "tail_speed_mean_m_s": -8.062859436766136e-05,
  "tail_speed_rms_m_s": 8.187129564352084e-05,
  "tail_sensor_speed_mean_m_s": -8.01577047944963e-05,
  "tail_fk_speed_mean_m_s": -8.050905901366908e-05,
  "peak_tilt_rad": 0.08457155573092878,
  "peak_wheel_torque_nm": 0.4679277241230011,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5475248479650113,
  "final_integral_m_s": 0.5475248479650113,
  "elapsed_wall_s": 45.90238954400411
}
```
