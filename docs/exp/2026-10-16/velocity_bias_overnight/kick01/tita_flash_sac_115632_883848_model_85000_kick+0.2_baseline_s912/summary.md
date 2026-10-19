# tita_flash_sac_115632_883848_model_85000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "3146ae41a897386d9315f3b0cc8706649c01b9109aa733713d29a8cf8794c4f6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.602173034895539,
  "max_drift_m": 7.602173034895539,
  "radial_IAE_m_s": 229.14613388693826,
  "signed_longitudinal_delta_m": 7.588167238427519,
  "tail_speed_mean_m_s": 0.1275095165303146,
  "tail_speed_rms_m_s": 0.12751112552884933,
  "tail_sensor_speed_mean_m_s": 0.12723378231131138,
  "tail_fk_speed_mean_m_s": 0.12723396274064902,
  "peak_tilt_rad": 0.0820722354341683,
  "peak_wheel_torque_nm": 1.9681578874588013,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.708962158998474
}
```
