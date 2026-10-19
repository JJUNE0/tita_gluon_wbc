# tita_flash_sac_115632_883848_model_85000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "bea504ef41a76e133ca0f072e75b210033a3e6265a82cc0a82c8806cbb1de654",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.223561838891884,
  "max_drift_m": 7.223561838891884,
  "radial_IAE_m_s": 207.37766933003667,
  "signed_longitudinal_delta_m": 7.212993490632819,
  "tail_speed_mean_m_s": 0.1272523382822961,
  "tail_speed_rms_m_s": 0.12725409511690539,
  "tail_sensor_speed_mean_m_s": 0.1269772223290275,
  "tail_fk_speed_mean_m_s": 0.12697740592671122,
  "peak_tilt_rad": 0.06728482926948653,
  "peak_wheel_torque_nm": 2.0954337120056152,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 19.235179229988717
}
```
