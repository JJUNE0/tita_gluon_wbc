# tita_flash_sac_115632_883848_model_30000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "188e6c9672dfe6187b8b5516fb284d475aa018fd1d540029e291d54aa5654e8e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020716618527668585,
  "max_drift_m": 0.11456356568752948,
  "radial_IAE_m_s": 1.4685234209399307,
  "signed_longitudinal_delta_m": -0.02070805578500265,
  "tail_speed_mean_m_s": 1.6860680532544537e-05,
  "tail_speed_rms_m_s": 3.5252003398458944e-05,
  "tail_sensor_speed_mean_m_s": 1.546995554395721e-05,
  "tail_fk_speed_mean_m_s": 1.7350315499173846e-05,
  "peak_tilt_rad": 0.12856210042420746,
  "peak_wheel_torque_nm": 0.7998212575912476,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5644631855224544,
  "final_integral_m_s": 0.5644631855224544,
  "elapsed_wall_s": 12.787474293960258
}
```
