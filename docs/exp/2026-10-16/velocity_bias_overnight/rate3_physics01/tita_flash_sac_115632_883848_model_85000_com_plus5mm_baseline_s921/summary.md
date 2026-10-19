# tita_flash_sac_115632_883848_model_85000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "bf7685ffae79b2ed5e3c3f0050d35f94ea229c1a7efa428d057d98c8eb65943d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.33607457677229,
  "max_drift_m": 8.33607457677229,
  "radial_IAE_m_s": 246.04797379646408,
  "signed_longitudinal_delta_m": 8.314253625021694,
  "tail_speed_mean_m_s": 0.142720886561093,
  "tail_speed_rms_m_s": 0.1427220987176759,
  "tail_sensor_speed_mean_m_s": 0.14241232258416978,
  "tail_fk_speed_mean_m_s": 0.14241237304469018,
  "peak_tilt_rad": 0.06653755871552658,
  "peak_wheel_torque_nm": 0.14694923162460327,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.170289843983483
}
```
