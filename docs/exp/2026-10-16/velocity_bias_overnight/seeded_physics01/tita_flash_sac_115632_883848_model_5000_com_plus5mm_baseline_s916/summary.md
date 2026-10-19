# tita_flash_sac_115632_883848_model_5000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "35dd6079a79012d8fa72a5955d083ce871bcab8ad281ebc2e0e408dc9ffadd54",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.348479334780839,
  "max_drift_m": 9.348479334780839,
  "radial_IAE_m_s": 282.75920393037376,
  "signed_longitudinal_delta_m": -8.936148429560513,
  "tail_speed_mean_m_s": -0.15740587966401834,
  "tail_speed_rms_m_s": 0.15883648138920212,
  "tail_sensor_speed_mean_m_s": -0.1599589157416675,
  "tail_fk_speed_mean_m_s": -0.15659551170394362,
  "peak_tilt_rad": 0.06404171364378142,
  "peak_wheel_torque_nm": 3.8010849952697754,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.669509953004308
}
```
