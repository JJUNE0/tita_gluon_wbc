# tita_flash_sac_115632_883848_model_75000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
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
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "d644e173dfab560f6dd02970c9aa1c76d8d957d5ac32a49ca90aa17d416923d7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03842437779335243,
  "max_drift_m": 0.04960684546933817,
  "radial_IAE_m_s": 2.2117337225567564,
  "signed_longitudinal_delta_m": 0.038421116746856596,
  "tail_speed_mean_m_s": 3.4547816687799534e-05,
  "tail_speed_rms_m_s": 3.608386442608425e-05,
  "tail_sensor_speed_mean_m_s": 3.455875162115102e-05,
  "tail_fk_speed_mean_m_s": 3.520128992114395e-05,
  "peak_tilt_rad": 0.06695134255862523,
  "peak_wheel_torque_nm": 0.3509487807750702,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.006532011806692683,
  "final_integral_m_s": 0.006532011806692683,
  "elapsed_wall_s": 16.08909574203426
}
```
