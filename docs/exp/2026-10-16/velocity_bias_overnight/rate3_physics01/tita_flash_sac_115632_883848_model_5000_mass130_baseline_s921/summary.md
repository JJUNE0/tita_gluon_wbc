# tita_flash_sac_115632_883848_model_5000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "42fea1ed4e0de95d6350429d0bafd931a804eff598e1ac67322a56f0244ba3c4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.5993341939548733,
  "max_drift_m": 2.5993341939548733,
  "radial_IAE_m_s": 77.63407486366009,
  "signed_longitudinal_delta_m": -2.5980737798011555,
  "tail_speed_mean_m_s": -0.04372756636575938,
  "tail_speed_rms_m_s": 0.048737377021189784,
  "tail_sensor_speed_mean_m_s": -0.044219342980106977,
  "tail_fk_speed_mean_m_s": -0.04331245456119808,
  "peak_tilt_rad": 0.1523302018380095,
  "peak_wheel_torque_nm": 4.494125843048096,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.748931054957211
}
```
