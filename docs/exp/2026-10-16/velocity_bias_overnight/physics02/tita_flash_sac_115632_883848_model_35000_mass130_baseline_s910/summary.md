# tita_flash_sac_115632_883848_model_35000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "cc57cf124ce3fe96700879a0121e162f799ab0ce18027aae9cf0f948eaa89a2a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.1593608912705566,
  "max_drift_m": 1.1593608912705566,
  "radial_IAE_m_s": 33.81030915016353,
  "signed_longitudinal_delta_m": 1.1586446303034357,
  "tail_speed_mean_m_s": 0.020321088157584502,
  "tail_speed_rms_m_s": 0.0203225236265718,
  "tail_sensor_speed_mean_m_s": 0.020277428497935176,
  "tail_fk_speed_mean_m_s": 0.020277651130303293,
  "peak_tilt_rad": 0.12207659378879554,
  "peak_wheel_torque_nm": 0.7105944752693176,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.355412540957332
}
```
