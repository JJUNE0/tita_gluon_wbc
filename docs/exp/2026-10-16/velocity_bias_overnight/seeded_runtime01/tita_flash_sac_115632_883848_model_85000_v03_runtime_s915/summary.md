# tita_flash_sac_115632_883848_model_85000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "db9402098d041d4f8e2f04ba611475bf487c490413aa68fd648cdfe0ca5386c3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09473242742452115,
  "max_drift_m": 0.1067532472891883,
  "radial_IAE_m_s": 5.63633574510129,
  "signed_longitudinal_delta_m": 0.09473018158631778,
  "tail_speed_mean_m_s": 3.0962676822593346e-06,
  "tail_speed_rms_m_s": 9.698382000642726e-06,
  "tail_sensor_speed_mean_m_s": 3.1371456476735755e-06,
  "tail_fk_speed_mean_m_s": 3.4645409778334494e-06,
  "peak_tilt_rad": 0.06505940509637176,
  "peak_wheel_torque_nm": 0.4460051953792572,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5828646020620942,
  "final_integral_m_s": 0.5828646020620942,
  "elapsed_wall_s": 14.91005441499874
}
```
