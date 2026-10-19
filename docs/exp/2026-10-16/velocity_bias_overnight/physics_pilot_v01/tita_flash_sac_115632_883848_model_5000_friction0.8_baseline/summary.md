# tita_flash_sac_115632_883848_model_5000_friction0.8_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_friction0.8_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "e1ec80d8a87fdaefb677eda567076b89fc754a7c3139c4d77a76043b92aeea4e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.034129412535068,
  "max_drift_m": 10.034129412535068,
  "radial_IAE_m_s": 304.0433141969262,
  "signed_longitudinal_delta_m": -9.392981454549473,
  "tail_speed_mean_m_s": -0.16902646760405723,
  "tail_speed_rms_m_s": 0.17025668145252434,
  "tail_sensor_speed_mean_m_s": -0.16840137109411016,
  "tail_fk_speed_mean_m_s": -0.16823284194499286,
  "peak_tilt_rad": 0.07320076327241343,
  "peak_wheel_torque_nm": 3.8801331520080566,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.568839531973936
}
```
