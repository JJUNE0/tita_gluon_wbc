# tita_flash_sac_115632_883848_model_5000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "f0493eceaeb0d984b797dd6231c2ae7ed80e362c6ac6aaaae4a945f80a2fd99a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.80759612396533,
  "max_drift_m": 10.80759612396533,
  "radial_IAE_m_s": 327.5800517828768,
  "signed_longitudinal_delta_m": -10.196595381008049,
  "tail_speed_mean_m_s": -0.18203093458337521,
  "tail_speed_rms_m_s": 0.183014817202988,
  "tail_sensor_speed_mean_m_s": -0.17941298367677963,
  "tail_fk_speed_mean_m_s": -0.18133054279310198,
  "peak_tilt_rad": 0.08238100455327468,
  "peak_wheel_torque_nm": 3.8849568367004395,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.580459426972084
}
```
