# tita_flash_sac_115632_883848_model_55000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
  },
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "3e4dec8a60c93cdc9147c6bf6b23fa21112592599da84d97d4586d1265122129",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02132293835317821,
  "max_drift_m": 0.04695677388366297,
  "radial_IAE_m_s": 1.3984992236410039,
  "signed_longitudinal_delta_m": 0.02131882338235948,
  "tail_speed_mean_m_s": -6.173824086057345e-05,
  "tail_speed_rms_m_s": 0.004187607816685342,
  "tail_sensor_speed_mean_m_s": -0.00020256863274491102,
  "tail_fk_speed_mean_m_s": -8.062590056155365e-06,
  "peak_tilt_rad": 0.090793802134151,
  "peak_wheel_torque_nm": 1.2701420783996582,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08621865118613135,
  "final_integral_m_s": 0.20361058065587712,
  "elapsed_wall_s": 4.328686160966754
}
```
