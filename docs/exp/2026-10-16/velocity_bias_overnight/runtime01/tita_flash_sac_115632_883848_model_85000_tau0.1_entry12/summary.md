# tita_flash_sac_115632_883848_model_85000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "733defb3359ad88af078d0fad031ab860dd3d45cdd8af44fc595ffb0de58dc48",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.057476042013301934,
  "max_drift_m": 0.06581325244125275,
  "radial_IAE_m_s": 3.4359535995660546,
  "signed_longitudinal_delta_m": 0.057472129246964605,
  "tail_speed_mean_m_s": -2.229589602726063e-06,
  "tail_speed_rms_m_s": 4.161436951580507e-06,
  "tail_sensor_speed_mean_m_s": -2.190269023979605e-06,
  "tail_fk_speed_mean_m_s": -1.8872387075925695e-06,
  "peak_tilt_rad": 0.065457474256575,
  "peak_wheel_torque_nm": 0.49968403577804565,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.58253514978793,
  "final_integral_m_s": 0.582526911720655,
  "elapsed_wall_s": 5.888071849010885
}
```
