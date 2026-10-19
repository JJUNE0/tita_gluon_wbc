# tita_flash_sac_115632_883848_model_85000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "480c02ff4beaa07e87569e1b75ea596378e5a07f028180a53d855fc20cb6ad88",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09450059721248086,
  "max_drift_m": 0.106545124914217,
  "radial_IAE_m_s": 5.628775651922133,
  "signed_longitudinal_delta_m": 0.09449876568409518,
  "tail_speed_mean_m_s": -7.493617330449186e-06,
  "tail_speed_rms_m_s": 1.0518646178809758e-05,
  "tail_sensor_speed_mean_m_s": -7.4403147821054634e-06,
  "tail_fk_speed_mean_m_s": -7.149798855155379e-06,
  "peak_tilt_rad": 0.06529361699133496,
  "peak_wheel_torque_nm": 0.4435630440711975,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5824561679677,
  "final_integral_m_s": 0.5824561679677,
  "elapsed_wall_s": 13.074700632016174
}
```
