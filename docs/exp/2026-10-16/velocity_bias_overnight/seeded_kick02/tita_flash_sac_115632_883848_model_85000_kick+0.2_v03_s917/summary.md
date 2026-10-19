# tita_flash_sac_115632_883848_model_85000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "85772d58d24ff10728334de5a3ac66d06f4111ace138ba5f330e2b5919cf8585",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09581085351436784,
  "max_drift_m": 0.1678264293951762,
  "radial_IAE_m_s": 5.880695899260534,
  "signed_longitudinal_delta_m": 0.09580851857193103,
  "tail_speed_mean_m_s": -5.266445043624925e-06,
  "tail_speed_rms_m_s": 1.0110790197305687e-05,
  "tail_sensor_speed_mean_m_s": -5.2157004845129584e-06,
  "tail_fk_speed_mean_m_s": -4.9171668606244765e-06,
  "peak_tilt_rad": 0.08118035910289767,
  "peak_wheel_torque_nm": 2.0778448581695557,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5825343089631975,
  "final_integral_m_s": 0.5825343089631975,
  "elapsed_wall_s": 9.25097882800037
}
```
