# tita_flash_sac_115632_883848_model_5000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "3de754766ece3a7068698a52b23c395d7993f67f65020d70aee02d5ae8aa6f03",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.7731585599249513,
  "max_drift_m": 3.7731585599249513,
  "radial_IAE_m_s": 97.56208055986006,
  "signed_longitudinal_delta_m": -3.7441161605885256,
  "tail_speed_mean_m_s": -0.0811421147130824,
  "tail_speed_rms_m_s": 0.08244552039083237,
  "tail_sensor_speed_mean_m_s": -0.08042799529260862,
  "tail_fk_speed_mean_m_s": -0.0810510329642924,
  "peak_tilt_rad": 0.1408432546254934,
  "peak_wheel_torque_nm": 3.014334201812744,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.366685405024327
}
```
