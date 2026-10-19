# tita_flash_sac_115632_883848_model_85000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "09fec977da81e84890525aecb5f25dd4a9b6d648823f9f72f4f27234c44ace1b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.419333738747022,
  "max_drift_m": 7.419333738747022,
  "radial_IAE_m_s": 218.47363536807083,
  "signed_longitudinal_delta_m": 7.408695566593396,
  "tail_speed_mean_m_s": 0.1274398635874964,
  "tail_speed_rms_m_s": 0.12744151017651806,
  "tail_sensor_speed_mean_m_s": 0.12716431158889616,
  "tail_fk_speed_mean_m_s": 0.1271644772420818,
  "peak_tilt_rad": 0.06728149799849925,
  "peak_wheel_torque_nm": 0.1576998233795166,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.082992005045526
}
```
