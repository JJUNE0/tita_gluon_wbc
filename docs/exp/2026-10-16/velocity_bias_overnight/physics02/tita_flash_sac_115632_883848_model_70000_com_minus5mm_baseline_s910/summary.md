# tita_flash_sac_115632_883848_model_70000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
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
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "23dedde4d54d6620df8a90d3c844e4bc1718cb479df9ab54733b0ad8d45c180b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.650950032261565,
  "max_drift_m": 5.650950032261565,
  "radial_IAE_m_s": 169.51798341643445,
  "signed_longitudinal_delta_m": -5.614613752580914,
  "tail_speed_mean_m_s": -0.09414975900447711,
  "tail_speed_rms_m_s": 0.09414979841172076,
  "tail_sensor_speed_mean_m_s": -0.09394600498011668,
  "tail_fk_speed_mean_m_s": -0.09394512088491482,
  "peak_tilt_rad": 0.017294274448654168,
  "peak_wheel_torque_nm": 0.11431953310966492,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.875941567996051
}
```
