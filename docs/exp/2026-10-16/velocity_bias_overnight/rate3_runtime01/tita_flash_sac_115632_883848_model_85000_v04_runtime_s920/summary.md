# tita_flash_sac_115632_883848_model_85000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "7a16a0f2184fc7f6856027288d40486d29e1484428da25eb9033614128ed7f15",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09462537760543481,
  "max_drift_m": 0.10666109595036996,
  "radial_IAE_m_s": 5.634982839047289,
  "signed_longitudinal_delta_m": 0.09462347787238458,
  "tail_speed_mean_m_s": -5.174072489371089e-06,
  "tail_speed_rms_m_s": 1.0110551505364304e-05,
  "tail_sensor_speed_mean_m_s": -5.1244247684846965e-06,
  "tail_fk_speed_mean_m_s": -4.824610690257462e-06,
  "peak_tilt_rad": 0.0652428957950919,
  "peak_wheel_torque_nm": 0.44263529777526855,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5825366596026997,
  "final_integral_m_s": 0.5825366596026997,
  "elapsed_wall_s": 12.555952096998226
}
```
