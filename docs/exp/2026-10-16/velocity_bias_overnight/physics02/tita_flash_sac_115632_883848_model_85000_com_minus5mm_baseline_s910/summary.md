# tita_flash_sac_115632_883848_model_85000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "652e7f2e4e00d10476f12b635b8c3bfae75f9d07eda14a12a2299e73f6783087",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.44720709591935,
  "max_drift_m": 6.44720709591935,
  "radial_IAE_m_s": 188.28500666701112,
  "signed_longitudinal_delta_m": 6.441256639738789,
  "tail_speed_mean_m_s": 0.11243938618471173,
  "tail_speed_rms_m_s": 0.11244473573797668,
  "tail_sensor_speed_mean_m_s": 0.11219636270110067,
  "tail_fk_speed_mean_m_s": 0.11219638280643322,
  "peak_tilt_rad": 0.06812086721632649,
  "peak_wheel_torque_nm": 0.19897392392158508,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.711665359034669
}
```
