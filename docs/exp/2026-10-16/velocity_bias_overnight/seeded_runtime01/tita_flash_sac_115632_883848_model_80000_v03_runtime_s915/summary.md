# tita_flash_sac_115632_883848_model_80000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "124e5ae3f6dbf1b8541650b98abfa73c1819a2abd0046e9c126159dd8acb5e87",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.13096585898276153,
  "max_drift_m": 0.13905899780523504,
  "radial_IAE_m_s": 7.541898106472587,
  "signed_longitudinal_delta_m": 0.13093175994292985,
  "tail_speed_mean_m_s": 0.00012496985552039707,
  "tail_speed_rms_m_s": 0.00013001297903886396,
  "tail_sensor_speed_mean_m_s": 0.00012455788230483512,
  "tail_fk_speed_mean_m_s": 0.00012487349395442392,
  "peak_tilt_rad": 0.08433556256323094,
  "peak_wheel_torque_nm": 0.7100188136100769,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8223740205706832,
  "final_integral_m_s": 0.8223740205706832,
  "elapsed_wall_s": 14.409757725952659
}
```
